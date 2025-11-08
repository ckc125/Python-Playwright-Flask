from playwright.async_api import async_playwright
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScreenshotService:
    def __init__(self):
        self.browser = None
        self.playwright = None
        self.is_initialized = False
    
    async def initialize(self):
        """初始化浏览器"""
        if not self.is_initialized:
            try:
                self.playwright = await async_playwright().start()
                self.browser = await self.playwright.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-dev-shm-usage']
                )
                self.is_initialized = True
                logger.info("浏览器初始化成功")
            except Exception as e:
                logger.error(f"浏览器初始化失败: {str(e)}")
                self.is_initialized = False
                raise
    
    async def capture_screenshot_async(self, url, filepath, full_page=True, width=1920, format='png'):
        """异步截图函数"""
        context = None
        page = None
        
        try:
            # 每次截图前都重新初始化浏览器，确保连接正常
            await self.cleanup()
            await self.initialize()
            
            # 检查浏览器是否成功初始化
            if not self.browser:
                raise Exception("浏览器初始化失败")
            
            # 检查浏览器连接状态
            try:
                if not self.browser.is_connected():
                    raise Exception("浏览器连接已断开")
            except Exception:
                # 如果检查连接状态失败，重新初始化
                await self.cleanup()
                await self.initialize()
                
                if not self.browser:
                    raise Exception("浏览器重新初始化失败")
            
            # 计算高度（基于宽高比）
            height = int(width * 9 / 16)  # 16:9 宽高比
            
            # 创建新页面
            context = await self.browser.new_context(
                viewport={'width': width, 'height': height},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                ignore_https_errors=True  # 忽略HTTPS证书错误
            )
            page = await context.new_page()
            
            # 设置超时（增加到120秒）
            page.set_default_timeout(120000)
            
            # 智能页面加载策略
            logger.info(f"正在访问: {url}")
            
            # 尝试多种加载策略
            load_strategies = [
                {'wait_until': 'domcontentloaded', 'timeout': 30000},
                {'wait_until': 'load', 'timeout': 30000},
                {'wait_until': 'networkidle', 'timeout': 30000}
            ]
            
            last_error = None
            for i, strategy in enumerate(load_strategies):
                try:
                    logger.info(f"尝试策略 {i+1}: {strategy['wait_until']}")
                    await page.goto(url, wait_until=strategy['wait_until'], timeout=strategy['timeout'])
                    logger.info("页面加载成功")
                    last_error = None
                    break
                except Exception as e:
                    last_error = e
                    logger.warning(f"策略 {i+1} 失败: {str(e)}")
                    if i < len(load_strategies) - 1:
                        logger.info("尝试下一个策略...")
                    continue
            
            # 如果所有策略都失败
            if last_error:
                raise last_error
            
            # 等待页面稳定（减少等待时间）
            await page.wait_for_timeout(1000)
            
            # 根据格式进行截图
            logger.info(f"正在截图: {filepath} (格式: {format})")
            
            if format == 'pdf':
                # PDF截图
                await page.pdf(path=filepath, format='A4', print_background=True)
            elif format == 'gif':
                # GIF格式需要特殊处理 - 这里我们使用PNG然后转换
                # 先截图为PNG，然后转换为GIF
                temp_file = filepath.replace('.gif', '.png')
                await page.screenshot(path=temp_file, full_page=full_page)
                
                # 使用PIL将PNG转换为GIF
                try:
                    from PIL import Image
                    img = Image.open(temp_file)
                    img = img.convert('P', palette=Image.ADAPTIVE, colors=256)
                    img.save(filepath, 'GIF')
                    
                    # 删除临时文件
                    import os
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                except Exception as e:
                    logger.error(f"GIF转换失败: {str(e)}")
                    # 如果GIF转换失败，直接使用PNG文件
                    import shutil
                    shutil.copy2(temp_file, filepath.replace('.gif', '.png'))
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                    return {"success": False, "error": f"GIF转换失败: {str(e)}"}
            else:
                # PNG/JPG截图
                screenshot_options = {
                    'path': filepath,
                    'full_page': full_page
                }
                
                if format == 'jpg':
                    screenshot_options['quality'] = 85  # JPG质量
                
                await page.screenshot(**screenshot_options)
            
            # 关闭页面和上下文
            await page.close()
            await context.close()
            
            logger.info(f"截图成功: {filepath}")
            return {"success": True, "filepath": filepath}
            
        except Exception as e:
            logger.error(f"截图失败: {str(e)}")
            # 清理资源
            try:
                if page:
                    await page.close()
                if context:
                    await context.close()
            except Exception as cleanup_error:
                logger.warning(f"资源清理失败: {str(cleanup_error)}")
            return {"success": False, "error": str(e)}
    
    def capture_screenshot(self, url, filepath, full_page=True, width=1920, format='png'):
        """同步截图接口"""
        try:
            # 创建新的事件循环
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # 运行异步函数
            result = loop.run_until_complete(self.capture_screenshot_async(url, filepath, full_page, width, format))
            loop.close()
            return result
        except Exception as e:
            logger.error(f"截图服务异常: {str(e)}")
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