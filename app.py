#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import uuid
import subprocess
import json
from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')
GABCTK = os.path.join(BASE_DIR, 'gabctk.py')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    f = request.files['file']
    if f.filename == '' or not f.filename.lower().endswith('.gabc'):
        return jsonify({'error': 'Please upload a .gabc file'}), 400

    tempo = request.form.get('tempo', '165')
    transpose = request.form.get('transpose', '')

    uid = str(uuid.uuid4())[:8]
    safe_name = secure_filename(f.filename)
    base_name = os.path.splitext(safe_name)[0]

    gabc_path = os.path.join(UPLOAD_FOLDER, f'{uid}_{safe_name}')
    midi_path = os.path.join(OUTPUT_FOLDER, f'{uid}_{base_name}.mid')

    f.save(gabc_path)

    cmd = [sys.executable, GABCTK, '-i', gabc_path, '-o', midi_path, '-t', tempo]
    if transpose:
        cmd += ['-d', transpose]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30,
                                cwd=BASE_DIR)
        if result.returncode != 0 or not os.path.exists(midi_path):
            err = result.stderr or result.stdout or 'Conversion failed'
            return jsonify({'error': err}), 500
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Conversion timed out'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'success': True,
        'midi_id': f'{uid}_{base_name}',
        'filename': f'{base_name}.mid'
    })

@app.route('/midi/<midi_id>')
def get_midi(midi_id):
    # Validate no path traversal
    safe = secure_filename(midi_id)
    path = os.path.join(OUTPUT_FOLDER, f'{safe}.mid')
    if not os.path.exists(path):
        return jsonify({'error': 'MIDI not found'}), 404
    return send_file(path, mimetype='audio/midi', as_attachment=True,
                     download_name=f'{safe}.mid')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
