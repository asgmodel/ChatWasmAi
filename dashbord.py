import gradio as gr
import modelscope_studio.components.antd as antd
import modelscope_studio.components.base as ms
import modelscope_studio.components.pro as pro

with gr.Blocks() as demo, ms.Application(), antd.ConfigProvider():
    pro.WebSandbox(
        value={
            "./index.html":
            """
            
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wasm - شاشة تمهيدية بيضاء</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Tajawal', sans-serif;
            overflow: hidden;
        }
        .light-mint {
            background-color: #d4f1e6;
        }
        .text-mint {
            color: #1abc9c;
        }
        
        /* شاشة التحميل */
        #splash-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: #ffffff; /* خلفية بيضاء */
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            transition: opacity 1s ease-out, transform 1.2s ease-out;
        }
        
        .splash-content {
            text-align: center;
            color: #333333; /* لون نص غامق */
            padding: 2rem;
            position: relative;
        }
        
        .logo-container {
            position: relative;
            width: 150px;
            height: 150px;
            margin: 0 auto 2rem;
        }
        
        .logo-icon {
            width: 100%;
            height: 100%;
            color: #1abc9c; /* لون المينت للأيقونة */
            animation: pulse 2s infinite, rotate 8s linear infinite;
            filter: drop-shadow(0 5px 15px rgba(26, 188, 156, 0.3));
        }
        
        .logo-circle {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: 3px solid rgba(26, 188, 156, 0.2); /* لون المينت بشفافية */
            border-radius: 50%;
            animation: expand 3s ease-in-out infinite;
        }
        
        .logo-circle:nth-child(2) {
            animation-delay: 1s;
        }
        
        .logo-circle:nth-child(3) {
            animation-delay: 2s;
        }
        
        .splash-text {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: #333333; /* لون نص غامق */
            opacity: 0;
            transform: translateY(20px);
            animation: fadeInUp 1s forwards 0.5s;
        }
        
        .splash-subtext {
            font-size: 1.2rem;
            margin-bottom: 2rem;
            color: #666666; /* لون نص متوسط */
            opacity: 0;
            transform: translateY(20px);
            animation: fadeInUp 1s forwards 1s;
        }
        
        .progress-container {
            width: 300px;
            height: 6px;
            background: rgba(26, 188, 156, 0.2); /* لون المينت بشفافية */
            border-radius: 10px;
            overflow: hidden;
            margin: 2rem auto;
        }
        
        .progress-bar {
            height: 100%;
            width: 0%;
            background: #1abc9c; /* لون المينت */
            border-radius: 10px;
            transition: width 0.4s ease;
        }
        
        .splash-tip {
            margin-top: 1.5rem;
            font-size: 0.9rem;
            color: #888888; /* لون نص فاتح */
            opacity: 0;
            animation: fadeIn 1s forwards 2s;
        }
        
        /* المحتوى الرئيسي - مخفي في البداية */
        #main-content {
            opacity: 0;
            transition: opacity 1s ease-in;
        }
        
        /* تأثيرات للشاشة الرئيسية */
        .main-icon {
            transition: all 0.5s ease;
            color: #1abc9c; /* لون المينت */
        }
        
        .main-icon:hover {
            transform: scale(1.1);
            filter: drop-shadow(0 8px 20px rgba(26, 188, 156, 0.4));
        }
        
        .nav-link {
            position: relative;
            color: #4a5568; /* لون رمادي يتناسب مع التصميم */
        }
        
        .nav-link::after {
            content: '';
            position: absolute;
            bottom: -5px;
            right: 0;
            width: 0;
            height: 2px;
            background-color: #1abc9c; /* لون المينت */
            transition: width 0.3s ease;
        }
        
        .nav-link:hover::after {
            width: 100%;
        }
        
        .nav-link:hover {
            color: #1abc9c; /* لون المينت */
        }
        
        .social-icon {
            transition: all 0.3s ease;
            color: #1abc9c; /* لون المينت */
        }
        
        .social-icon:hover {
            transform: translateY(-3px);
            color: #16a085; /* لون مينت أغمق قليلاً */
        }
        
        /* Animations */
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @keyframes expand {
            0% {
                transform: scale(1);
                opacity: 1;
            }
            100% {
                transform: scale(1.5);
                opacity: 0;
            }
        }
        
        @keyframes fadeInUp {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeIn {
            to {
                opacity: 0.8;
            }
        }
        
        /* الخلفية المتحركة */
        .floating-particles {
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: -1;
        }
        
        .particle {
            position: absolute;
            background: rgba(26, 188, 156, 0.1); /* لون المينت بشفافية خفيفة */
            border-radius: 50%;
        }
    </style>
</head>
<body>
    <!-- الشاشة التمهيدية -->
    <div id="splash-screen">
        <div class="splash-content">
            <div class="logo-container">
                <i data-feather="cpu" class="logo-icon"></i>
                <div class="logo-circle"></div>
                <div class="logo-circle"></div>
                <div class="logo-circle"></div>
            </div>
            
            <h1 class="splash-text">مرحبًا بك في Wasm</h1>
            <p class="splash-subtext">نحو مستقبل أسرع بتقنية WebAssembly</p>
            
            <div class="progress-container">
                <div class="progress-bar" id="progress-bar"></div>
            </div>
            
            <p class="splash-tip">جاري تحميل المحتوى الرائع، انتظر قليلاً...</p>
        </div>
        
        <!-- جسيمات عائمة في الخلفية -->
        <div class="floating-particles" id="particles"></div>
    </div>

    <!-- المحتوى الرئيسي -->
    <div id="main-content" class="light-mint min-h-screen flex flex-col">
        <!-- Header -->
        <header class="bg-white shadow-sm py-4 px-6">
            <div class="container mx-auto flex justify-between items-center">
                <h1 class="text-2xl font-bold text-mint">Wasm</h1>
                <nav>
                    <ul class="flex space-x-6 space-x-reverse">
                        <li><a href="#" class="nav-link transition">الرئيسية</a></li>
                        <li><a href="#" class="nav-link transition">حول</a></li>
                        <li><a href="#" class="nav-link transition">اتصل بنا</a></li>
                    </ul>
                </nav>
            </div>
        </header>

        <!-- Main Content -->
        <main class="flex-grow flex items-center justify-center">
            <div class="text-center">
                <i data-feather="cpu" class="main-icon w-16 h-16 mx-auto mb-4"></i>
                <h2 class="text-3xl font-bold text-gray-800 mb-2">مرحبًا بكم في Wasm</h2>
                <p class="text-gray-600 max-w-md mx-auto">موقع مخصص لتقنية WebAssembly</p>
            </div>
        </main>

        <!-- Footer -->
        <footer class="bg-white py-6 px-4 shadow-inner">
            <div class="container mx-auto text-center">
                <p class="text-gray-600">© 2023 Wasm. جميع الحقوق محفوظة.</p>
                <div class="flex justify-center space-x-4 space-x-reverse mt-3">
                    <a href="#" class="social-icon hover:opacity-80"><i data-feather="twitter"></i></a>
                    <a href="#" class="social-icon hover:opacity-80"><i data-feather="github"></i></a>
                    <a href="#" class="social-icon hover:opacity-80"><i data-feather="linkedin"></i></a>
                </div>
            </div>
        </footer>
    </div>

    <script>
        // تهيئة Feather Icons
        feather.replace();
        
        // عناصر DOM
        const splashScreen = document.getElementById('splash-screen');
        const mainContent = document.getElementById('main-content');
        const progressBar = document.getElementById('progress-bar');
        
        // إنشاء الجسيمات العائمة
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            const colors = [
                'rgba(26, 188, 156, 0.1)', 
                'rgba(26, 188, 156, 0.07)', 
                'rgba(26, 188, 156, 0.05)'
            ];
            
            for (let i = 0; i < 15; i++) {
                const particle = document.createElement('div');
                particle.classList.add('particle');
                
                const size = Math.random() * 15 + 5;
                particle.style.width = `${size}px`;
                particle.style.height = `${size}px`;
                
                particle.style.left = `${Math.random() * 100}%`;
                particle.style.top = `${Math.random() * 100}%`;
                
                particle.style.background = colors[Math.floor(Math.random() * colors.length)];
                
                particlesContainer.appendChild(particle);
                
                // تحريك الجسيم
                moveParticle(particle);
            }
        }
        
        // تحريك الجسيمات
        function moveParticle(particle) {
            const duration = Math.random() * 10 + 10;
            
            particle.style.transition = `all ${duration}s linear`;
            
            setTimeout(() => {
                particle.style.left = `${Math.random() * 100}%`;
                particle.style.top = `${Math.random() * 100}%`;
                
                // استمرار الحركة
                setInterval(() => {
                    particle.style.left = `${Math.random() * 100}%`;
                    particle.style.top = `${Math.random() * 100}%`;
                }, duration * 1000);
                
            }, 100);
        }
        
        // محاكاة التقدم في التحميل
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 10;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
                
                // الانتقال إلى المحتوى الرئيسي بعد اكتمال التحميل
                setTimeout(showMainContent, 500);
            }
            progressBar.style.width = `${progress}%`;
        }, 300);
        
        // عرض المحتوى الرئيسي
        function showMainContent() {
            splashScreen.style.opacity = '0';
            splashScreen.style.transform = 'scale(1.1)';
            
            setTimeout(() => {
                splashScreen.style.display = 'none';
                mainContent.style.opacity = '1';
            }, 1000);
        }
        
        // بدء إنشاء الجسيمات عند تحميل الصفحة
        window.addEventListener('load', createParticles);
        
        // إمكانية تخطي الشاشة التمهيدية بالنقر
        splashScreen.addEventListener('click', () => {
            clearInterval(interval);
            progress = 100;
            progressBar.style.width = '100%';
            setTimeout(showMainContent, 300);
        });
    </script>
</body>
</html>
            """
        },
        template="html",
        height=600,
    )
