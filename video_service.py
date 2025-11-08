from playwright.async_api import async_playwright
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoService:
    def __init__(self):
        self.browser = None
        self.playwright = None
        self.is_initialized = False
    
    async def initialize(self):
        """初始化浏览器"""
        if not self.is_initialized:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            self.is_initialized = True
            logger.info("浏览器初始化成功")
    
    async def record_video_async(self, url, filepath, duration=10):
        """异步录制视频函数"""
        try:
            await self.initialize()
            
            # 创建新页面并开始录制
            context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                record_video_dir='output/videos',
                record_video_size={'width': 1920, 'height': 1080}
            )
            
            page = await context.new_page()
            
            # 设置超时
            page.set_default_timeout(30000)
            
            # 导航到页面
            logger.info(f"正在访问: {url}")
            await page.goto(url, wait_until='networkidle')
            
            # 等待页面加载完成
            await page.wait_for_timeout(2000)
            
            # 录制视频
            logger.info(f"开始录制视频，时长: {duration}秒")
            
            # 模拟一些用户交互（可选）
            await self.simulate_user_interaction(page)
            
            # 等待录制时长
            await asyncio.sleep(duration)
            
            # 停止录制
            await context.close()
            
            # 获取录制的视频文件
            video_path = page.video.path()
            
            # 重命名视频文件到指定路径
            import shutil
            shutil.move(video_path, filepath)
            
            logger.info(f"视频录制成功: {filepath}")
            return {"success": True, "filepath": filepath}
            
        except Exception as e:
            logger.error(f"视频录制失败: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def simulate_user_interaction(self, page):
        """模拟用户交互，让视频更有内容"""
        try:
            # 滚动页面
            await page.evaluate("""
                window.scrollTo({
                    top: document.body.scrollHeight,
                    behavior: 'smooth'
                });
            """)
            
            await asyncio.sleep(1)
            
            # 滚动回顶部
            await page.evaluate("""
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            """)
            
            await asyncio.sleep(1)
            
            # 尝试点击第一个链接（如果有的话）
            try:
                await page.click('a:first-of-type', timeout=2000)
                await asyncio.sleep(1)
                await page.go_back()
            except:
                pass
                
        except Exception as e:
            logger.warning(f"用户交互模拟失败: {str(e)}")
    
    def record_video(self, url, filepath, duration=10):
        """同步录制视频接口"""
        try:
            # 运行异步函数
            result = asyncio.run(self.record_video_async(url, filepath, duration))
            return result
        except Exception as e:
            logger.error(f"视频录制服务异常: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def cleanup(self):
        """清理资源"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        self.is_initialized = False
        logger.info("浏览器资源已清理")
    
    def __del__(self):
        """析构函数"""
        if self.is_initialized:
            try:
                asyncio.run(self.cleanup())
            except:
                pass