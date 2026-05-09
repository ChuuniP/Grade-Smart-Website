const { execFile } = require('child_process');
const path = require('path');
const fs = require('fs/promises');

class OMRService {
  async processImage(imagePath) {
    imagePath = path.resolve(imagePath);
    await fs.access(imagePath);

    const scriptPath = path.join(__dirname, '..', '..', 'ref', 'mainOmr.py');
    const scriptCwd = path.dirname(scriptPath);
    const pythonCandidates = [
      { command: process.env.PYTHON || 'python', args: ['-X', 'utf8', scriptPath, imagePath] },
      { command: 'py', args: ['-3', '-X', 'utf8', scriptPath, imagePath] },
      { command: 'python3', args: ['-X', 'utf8', scriptPath, imagePath] },
      { command: 'python3.10', args: ['-X', 'utf8', scriptPath, imagePath] },
      { command: 'python3.11', args: ['-X', 'utf8', scriptPath, imagePath] }
    ];

    const runPython = ({ command, args }) => {
      return new Promise((resolve, reject) => {
        execFile(command, args, {
          cwd: scriptCwd,
          maxBuffer: 20 * 1024 * 1024,
          encoding: 'utf8',
          env: {
            ...process.env,
            PYTHONIOENCODING: 'utf-8'
          }
        }, (error, stdout, stderr) => {
          if (error) {
            return reject({ error, stderr: stderr, command });
          }
          resolve(stdout);
        });
      });
    };

    let lastError;
    for (const pythonCmd of pythonCandidates) {
      try {
        const stdout = await runPython(pythonCmd);
        return JSON.parse(stdout);
      } catch (err) {
        lastError = err;
        if (!err.error || err.error.code !== 'ENOENT') {
          break;
        }
      }
    }

    const message = lastError && lastError.stderr
      ? `Python OMR processing failed: ${lastError.stderr.trim()}`
      : 'Không tìm thấy Python để chạy script OMR. Vui lòng cài Python 3 và đảm bảo lệnh "python" hoặc "py" có trong PATH.';

    throw new Error(message);
  }
}

module.exports = new OMRService();
