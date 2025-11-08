from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import os
import uuid
from datetime import datetime
from screenshot_service import ScreenshotService
from video_service import VideoService

app = Flask(__name__)
CORS(app)

# 创建输出目录
os.makedirs('output/screenshots', exist_ok=True)
os.makedirs('output/videos', exist_ok=True)

screenshot_service = ScreenshotService()
video_service = VideoService()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api')
def api_info():
    return {
        "message": "网页截图和录屏服务",
        "endpoints": {
            "/screenshot": "POST - 截图网页",
            "/record": "POST - 录制网页视频",
            "/download/<filename>": "GET - 下载文件"
        }
    }

@app.route('/screenshot', methods=['POST'])
def take_screenshot():
    try:
        data = request.json
        url = data.get('url')
        full_page = data.get('full_page', True)
        width = data.get('width', 1920)
        image_format = data.get('format', 'png')  # 避免使用内置函数名
        
        if not url:
            return jsonify({"error": "URL不能为空"}), 400
        
        if width < 800 or width > 3840:
            return jsonify({"error": "宽度必须在800-3840像素之间"}), 400
        
        if image_format not in ['png', 'jpg', 'pdf', 'gif']:
            return jsonify({"error": "不支持的格式，请选择png、jpg、pdf或gif"}), 400
        
        # 根据格式生成文件名
        filename = f"screenshot_{uuid.uuid4().hex[:8]}_{int(datetime.now().timestamp())}.{image_format}"
        filepath = os.path.join('output', 'screenshots', filename)
        
        # 截图
        result = screenshot_service.capture_screenshot(url, filepath, full_page, width, image_format)
        
        if result['success']:
            return jsonify({
                "success": True,
                "filename": filename,
                "filepath": filepath,
                "download_url": f"/download/screenshots/{filename}",
                "message": "截图成功"
            })
        else:
            return jsonify({"error": result['error']}), 500
            
    except Exception as e:
        return jsonify({"error": f"截图失败: {str(e)}"}), 500

@app.route('/record', methods=['POST'])
def record_video():
    try:
        data = request.json
        url = data.get('url')
        duration = data.get('duration', 10)  # 默认10秒
        
        if not url:
            return jsonify({"error": "URL不能为空"}), 400
        
        if duration > 60:
            return jsonify({"error": "录制时长不能超过60秒"}), 400
        
        # 生成唯一文件名
        filename = f"video_{uuid.uuid4().hex[:8]}_{int(datetime.now().timestamp())}.webm"
        filepath = os.path.join('output', 'videos', filename)
        
        # 录制视频
        result = video_service.record_video(url, filepath, duration)
        
        if result['success']:
            return jsonify({
                "success": True,
                "filename": filename,
                "filepath": filepath,
                "download_url": f"/download/videos/{filename}",
                "message": "录制成功"
            })
        else:
            return jsonify({"error": result['error']}), 500
            
    except Exception as e:
        return jsonify({"error": f"录制失败: {str(e)}"}), 500

@app.route('/download/<filetype>/<filename>')
def download_file(filetype, filename):
    try:
        if filetype not in ['screenshots', 'videos']:
            return jsonify({"error": "文件类型错误"}), 400
            
        filepath = os.path.join('output', filetype, filename)
        
        if not os.path.exists(filepath):
            return jsonify({"error": "文件不存在"}), 404
            
        return send_file(filepath, as_attachment=True)
        
    except Exception as e:
        return jsonify({"error": f"下载失败: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)