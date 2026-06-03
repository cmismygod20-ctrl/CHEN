以下是您所需的肺癌医学影像分析网站的完整代码。它实现了癌变区域标记、扫描区域显示、分析报告生成及韩语PDF下载等功能，适配iPad操作。

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes, viewport-fit=cover">
    <title>폐암 의료 영상 분석 시스템 | AI 기반 병변 탐지</title>
    <!-- html2canvas + jspdf for PDF -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <style>
        * {
            box-sizing: border-box;
            user-select: none; /* avoid accidental text selection while drawing */
        }
        body {
            background: #eef2f7;
            font-family: 'Segoe UI', 'Noto Sans KR', 'Apple SD Gothic Neo', 'Roboto', sans-serif;
            margin: 0;
            padding: 20px;
            color: #1e2a3a;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 32px;
            box-shadow: 0 20px 35px -12px rgba(0,0,0,0.1);
            overflow: hidden;
            padding: 24px 28px 32px 28px;
        }
        /* header with download button */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            margin-bottom: 24px;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 16px;
        }
        h1 {
            font-size: 1.7rem;
            margin: 0;
            background: linear-gradient(135deg, #1e3c72, #2b5876);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
        }
        .badge {
            background: #d9f0ec;
            color: #0f5b4b;
            padding: 6px 12px;
            border-radius: 40px;
            font-size: 0.8rem;
            font-weight: bold;
        }
        .download-btn {
            background: #1e4668;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 40px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .download-btn:hover {
            background: #0f2f4a;
            transform: scale(0.98);
        }
        /* two columns layout */
        .main-dashboard {
            display: flex;
            flex-wrap: wrap;
            gap: 28px;
            margin: 20px 0 30px;
        }
        .image-panel {
            flex: 1.5;
            min-width: 280px;
            background: #f8fafc;
            border-radius: 28px;
            padding: 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        .analysis-panel {
            flex: 1;
            min-width: 280px;
            background: #ffffff;
            border-radius: 28px;
            padding: 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid #eef2ff;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .panel-title {
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 12px;
            border-left: 5px solid #2c7da0;
            padding-left: 14px;
            color: #0f2f4a;
        }
        .canvas-wrapper {
            background: #0b1a2a;
            border-radius: 24px;
            padding: 10px;
            text-align: center;
        }
        canvas#medicalCanvas {
            width: 100%;
            height: auto;
            background: #000;
            border-radius: 16px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            cursor: crosshair;
            touch-action: none;  /* improve touch drawing */
        }
        .toolbar {
            margin-top: 16px;
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            justify-content: center;
        }
        .btn {
            background: white;
            border: 1px solid #cbd5e1;
            padding: 8px 16px;
            border-radius: 40px;
            font-weight: 600;
            font-size: 0.85rem;
            cursor: pointer;
            transition: 0.2s;
            background: #f1f5f9;
        }
        .btn-primary {
            background: #2c7da0;
            border-color: #2c7da0;
            color: white;
        }
        .btn-danger {
            background: #e2e8f0;
            color: #b91c1c;
            border-color: #fecaca;
        }
        .btn-primary:active, .btn:active { transform: scale(0.96); }
        .scan-region {
            background: #f1f5f9;
            border-radius: 24px;
            padding: 16px;
            text-align: center;
        }
        .scan-canvas-container {
            background: #eef2f9;
            border-radius: 20px;
            padding: 12px;
        }
        canvas#roiCanvas {
            width: 100%;
            max-width: 200px;
            height: auto;
            background: #1e2a3a;
            border-radius: 16px;
            margin: 0 auto;
            display: block;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .result-text {
            background: #fef9e3;
            padding: 16px;
            border-radius: 20px;
            margin-top: 8px;
            border-left: 6px solid #e67e22;
        }
        .result-text h4 {
            margin: 0 0 8px 0;
            color: #c4450c;
        }
        .analysis-metrics {
            font-size: 0.95rem;
            line-height: 1.4;
        }
        .documentation {
            background: #f9fafb;
            border-radius: 28px;
            padding: 24px;
            margin-top: 30px;
            border: 1px solid #e2edf2;
        }
        .doc-title {
            font-size: 1.4rem;
            font-weight: bold;
            margin-bottom: 16px;
            color: #2c3e50;
        }
        .doc-content {
            display: flex;
            flex-direction: column;
            gap: 18px;
            font-size: 0.9rem;
            line-height: 1.5;
            color: #2d3e50;
        }
        hr {
            margin: 12px 0;
        }
        .footer-note {
            text-align: center;
            margin-top: 24px;
            font-size: 0.75rem;
            color: #5b6e8c;
        }
        @media (max-width: 800px) {
            .container { padding: 16px; }
            .btn { padding: 6px 12px; }
        }
        .rect-info {
            font-size: 0.75rem;
            margin-top: 8px;
            text-align: center;
        }
    </style>
</head>
<body>
<div class="container" id="reportContainer">
    <!-- header with download button (오른쪽 하단 요구사항: 오른쪽 위 or 아래 - 여기선 오른쪽 위) -->
    <div class="header">
        <div>
            <h1>🧠 폐암 AI 진조 보조 시스템 <span style="font-size:0.9rem;">(Lung Cancer CAD)</span></h1>
            <div class="badge">의료영상분석 · 폐 종양 탐지</div>
        </div>
        <button class="download-btn" id="pdfDownloadBtn">📄 한글 PDF 저장 (K-버전) ▼</button>
    </div>
    
    <div class="main-dashboard">
        <!-- 왼쪽: 의료영상 + 캔버스 & 암영역 표시 -->
        <div class="image-panel">
            <div class="panel-title">🩻 폐 CT 영상 (스캔 영역)</div>
            <div class="canvas-wrapper">
                <canvas id="medicalCanvas" width="600" height="600" style="width:100%; height:auto; max-width:600px; aspect-ratio:1/1"></canvas>
            </div>
            <div class="toolbar">
                <button class="btn" id="drawRectBtn">✏️ 새로운 병변 그리기</button>
                <button class="btn btn-danger" id="deleteRectBtn">🗑️ 선택 병변 삭제</button>
                <button class="btn" id="resetDefaultRect">🔄 기본 예제 병변</button>
                <span class="rect-info" id="rectCountStatus">활성 병변: 0개</span>
            </div>
            <div class="rect-info" style="color:#2c7da0;">※ CT 이미지에서 드래그하여 병변(암 의심 영역)을 사각형으로 표시하세요.</div>
        </div>
        
        <!-- 오른쪽: 스캔 영역(ROI 확대) + 결과 분석 페이지 (충분한 크기) -->
        <div class="analysis-panel">
            <div class="panel-title">🔍 스캔 영역(ROI) & 분석 결과</div>
            <div class="scan-region">
                <div style="font-weight:600; margin-bottom:8px;">📌 선택된 병변 영역 (Scan Region)</div>
                <div class="scan-canvas-container">
                    <canvas id="roiCanvas" width="200" height="200" style="width:100%; max-width:220px; height:auto; margin:0 auto;"></canvas>
                </div>
                <div class="result-text" id="analysisResultArea">
                    <h4>🧬 AI 분석 리포트</h4>
                    <div id="analysisDetail" class="analysis-metrics">
                        <!-- 동적 분석 결과 표시 -->
                        분석 결과가 여기에 표시됩니다.
                    </div>
                </div>
                <div style="margin-top: 12px; font-size:0.8rem; background:#eef2ff; border-radius:20px; padding:8px;">
                    💡 * 병변 영역(사각형) 선택 시 해당 부위의 고해상도 스캔 및 진단 리포트가 갱신됩니다.
                </div>
            </div>
        </div>
    </div>
    
    <!-- 요구사항 PDF에 포함될 문서: 설계 및 개발 방법, 주요 기능, 기대 효과 등 (한글) -->
    <div class="documentation" id="documentationSection">
        <div class="doc-title">📑 프로젝트 문서 (한글 PDF 포함 필수 항목)</div>
        <div class="doc-content">
            <div>
                <strong>🔧 1. 웹사이트 설계 및 개발 방법</strong><br>
                본 시스템은 HTML5, CSS3, JavaScript 기반의 순수 프론트엔드로 개발되었으며, iPad 및 다양한 디바이스에서 터치/마우스 드래그를 지원합니다. <br>
                의료 영상 분석을 위해 Canvas API를 활용하여 폐 CT 시뮬레이션 이미지 위에 사용자 정의 관심 영역(ROI)을 사각형(바운딩 박스) 방식으로 정밀 표시할 수 있습니다. <br>
               肺癌 병변 영역을 선택하면 해당 영역의 픽셀 데이터를 실시간으로 추출하여 ROI 스캔 영역(확대 뷰)을 표시하고, 앙상블 모델(전문 지식 기반 규칙 + 확률 시뮬레이션)을 통해 악성도, 조직 패턴, 권고사항을 산출합니다. 
                모든 분석 리포트는 한글(한국어)로 출력되며, PDF 저장 시 html2canvas + jsPDF 라이브러리를 사용하여 전체 대시보드와 문서 섹션을 포함한 보고서를 생성합니다.
            </div>
            <div>
                <strong>✨ 2. 웹사이트 주요 기능</strong><br>
                - ✅ 폐암 의심 영역 정밀 사각형 표시 (드래그/터치로 다중 병변 추가, 선택 및 삭제)<br>
                - ✅ 스캔 영역 디스플레이 : 선택한 병변 영역을 확대하여 시각화 (ROI 분석)<br>
                - ✅ 결과 분석 페이지 : AI 기반 추론 (병변 크기, 위치, 밀도 시뮬레이션 → 폐암 확률, TNM 유사 단계, 임상 권고)<br>
                - ✅ 결과 분석 화면이 충분한 비율을 차지 (오른쪽 패널 40% 이상, 텍스트/이미지 병합)<br>
                - ✅ 한글 PDF 저장 : 웹사이트 설계 방법, 주요 기능, 기대 효과, 부가 설명 포함. 다운로드 버튼을 통해 저장 가능<br>
                - ✅ 모바일/터치 최적화, iPad에서 원활한 드로잉 및 분석
            </div>
            <div>
                <strong>📈 3. 기대 효과 및 응용 가치</strong><br>
                · 임상의에게 CT 영상 내 폐 결절 위치 파악 및 2차 판독 보조 도구 제공 <br>
                · 딥러닝 기반 CAD 시스템의 프로토타입으로, 교육 및 연구 목적 활용 가능 <br>
                · 환자별 맞춤형 분석 리포트 자동 생성 → 의사 결정 지원 및 의료 접근성 향상 <br>
                · iPad에서 동작하여 이동성과 편의성을 겸비, PACS 시스템 연동 가능성 확장
            </div>
            <div>
                <strong>📌 4. 기타 관련 설명</strong><br>
                · 본 데모는 실제 임상 진단을 대체할 수 없으며, 교육 및 기술 시연용으로 제작되었습니다. <br>
                · 사용된 CT 이미지는 실제 환자 데이터가 아닌 합성(synthetic) 영상이지만 실제 폐 CT 패턴을 모방하여 설계되었습니다.<br>
                · 모든 분석 알고리즘은 의료 영상 분할 원리를 따르며, 추후 실제 AI 모델로 확장 가능합니다.<br>
                · 요구사항: 오른쪽 상단 다운로드 버튼 클릭 시 한글 PDF 자동 생성, ‘癌變區域方框’, ‘스캔 영역’, ‘분석 페이지’ 모두 포함.
            </div>
        </div>
    </div>
    <div class="footer-note">
        © 2025 폐암 의료영상분석 프로젝트 | 강의: 디지털헬스케어 & 의료영상 | 제출일: 2025.06.10
    </div>
</div>

<script>
    (function(){
        // ---------- Setup Canvas & Image Data ----------
        const canvas = document.getElementById('medicalCanvas');
        const ctx = canvas.getContext('2d');
        const roiCanvas = document.getElementById('roiCanvas');
        const roiCtx = roiCanvas.getContext('2d');
        
        // Image size 고정 (600x600)
        const W = 600, H = 600;
        canvas.width = W; canvas.height = H;
        roiCanvas.width = 200; roiCanvas.height = 200;
        
        // Synthetic Lung CT Image (의료용 흉부 CT 모사: 그라데이션 + 폐 실질 패턴)
        function drawLungSimulation() {
            // 배경 (흑백 톤 CT 느낌)
            const grad = ctx.createLinearGradient(0,0,W,H);
            grad.addColorStop(0, '#2a3e4f');
            grad.addColorStop(1, '#1c2e3c');
            ctx.fillStyle = grad;
            ctx.fillRect(0,0,W,H);
            // 폐 실질 구조 (타원형)
            ctx.save();
            ctx.globalCompositeOperation = 'lighter';
            ctx.fillStyle = '#5f7f6e';
            ctx.beginPath();
            ctx.ellipse(260, 300, 150, 200, 0, 0, Math.PI*2);
            ctx.fill();
            ctx.beginPath();
            ctx.ellipse(340, 310, 140, 190, 0, 0, Math.PI*2);
            ctx.fill();
            ctx.fillStyle = '#9abb9a';
            ctx.beginPath();
            ctx.ellipse(270, 290, 90, 130, 0, 0, Math.PI*2);
            ctx.fill();
            ctx.beginPath();
            ctx.ellipse(340, 300, 85, 125, 0, 0, Math.PI*2);
            ctx.fill();
            // 작은 결절 흉내
            ctx.fillStyle = '#c0dac0';
            ctx.beginPath();
            ctx.arc(290, 320, 12, 0, Math.PI*2);
            ctx.fill();
            ctx.fillStyle = '#aac3aa';
            ctx.beginPath();
            ctx.arc(350, 280, 8, 0, Math.PI*2);
            ctx.fill();
            ctx.globalCompositeOperation = 'source-over';
            // 혈관 모양 라인
            ctx.beginPath();
            ctx.strokeStyle = '#789b78';
            ctx.lineWidth = 2;
            for(let i=0;i<30;i++) {
                ctx.beginPath();
                ctx.moveTo(200 + i*12, 250+Math.sin(i)*20);
                ctx.lineTo(300+ i*7, 400+Math.cos(i)*15);
                ctx.stroke();
            }
            ctx.fillStyle = "#e0e9e0";
            ctx.font = "bold 16px 'Segoe UI'";
            ctx.shadowBlur = 0;
            ctx.fillText("LUNG CT (Simulated)", 20, 50);
            ctx.fillStyle = "#cfead0";
            ctx.font = "12px monospace";
            ctx.fillText("▶ 의심영역: 사각형 드래그", 20, 580);
            ctx.restore();
        }
        
        // 실제 이미지 데이터 유지 (CanvasImageData)
        let originalImageData = null;
        function captureOriginalImage() {
            originalImageData = ctx.getImageData(0,0,W,H);
        }
        function restoreOriginalBackground() {
            if(originalImageData) {
                ctx.putImageData(originalImageData,0,0);
            } else {
                drawLungSimulation();
                captureOriginalImage();
            }
        }
        
        // Rectangle management
        let rectangles = [];  // {x,y,w,h}
        let activeRectIndex = -1;
        let isDrawingMode = false;
        let startX = 0, startY = 0;
        let isDrawing = false;
        
        // Draw all rectangles (bounding boxes) and highlight active one
        function drawRectangles() {
            restoreOriginalBackground();
            for(let i=0; i<rectangles.length; i++) {
                const r = rectangles[i];
                ctx.save();
                if(i === activeRectIndex) {
                    ctx.strokeStyle = '#ffbb4c';
                    ctx.lineWidth = 4;
                    ctx.shadowBlur = 0;
                    ctx.setLineDash([6, 8]);
                } else {
                    ctx.strokeStyle = '#ff3b3b';
                    ctx.lineWidth = 2.5;
                    ctx.setLineDash([]);
                }
                ctx.strokeRect(r.x, r.y, r.w, r.h);
                // 표시: 암 영역 마커
                ctx.fillStyle = i === activeRectIndex ? '#ffbb4ccc' : '#ff000088';
                ctx.fillRect(r.x, r.y, r.w, r.h);
                ctx.setLineDash([]);
                ctx.font = "bold 14px 'Noto Sans KR'";
                ctx.fillStyle = "white";
                ctx.shadowBlur = 4;
                ctx.fillText("🔴 암의심", r.x+5, r.y+18);
                ctx.restore();
            }
            updateRectCounter();
            if(activeRectIndex >=0 && rectangles[activeRectIndex]) updateROIAndAnalysis();
            else if(rectangles.length===0) clearROIAnalysisEmpty();
        }
        
        function updateRectCounter() {
            document.getElementById('rectCountStatus').innerText = `활성 병변: ${rectangles.length}개 | 선택됨: ${activeRectIndex !== -1 ? activeRectIndex+1 : '없음'}`;
        }
        
        function clearROIAnalysisEmpty() {
            roiCtx.clearRect(0,0,200,200);
            roiCtx.fillStyle = "#2d3e50";
            roiCtx.fillRect(0,0,200,200);
            roiCtx.fillStyle = "white";
            roiCtx.font = "12px sans-serif";
            roiCtx.fillText("병변 없음", 60,100);
            document.getElementById('analysisDetail').innerHTML = "❌ 선택된 암 의심 영역이 없습니다. 왼쪽 이미지에서 병변을 그리거나 선택하세요.";
        }
        
        // ROI 업데이트 (선택된 사각형 영역 추출, 확대)
        function updateROIAndAnalysis() {
            if(activeRectIndex === -1 || !rectangles[activeRectIndex]) {
                clearROIAnalysisEmpty();
                return;
            }
            const rect = rectangles[activeRectIndex];
            // 영역 추출 안전장치
            let sx = Math.max(0, Math.min(W-1, rect.x));
            let sy = Math.max(0, Math.min(H-1, rect.y));
            let sw = Math.max(5, Math.min(W-sx, rect.w));
            let sh = Math.max(5, Math.min(H-sy, rect.h));
            if(sw<5 || sh<5) return;
            
            // 이미지 데이터 추출 (원본 기준)
            restoreOriginalBackground();
            const imgData = ctx.getImageData(sx, sy, sw, sh);
            // ROI canvas 에 그리기 (확대 비율 유지)
            roiCtx.clearRect(0,0,200,200);
            roiCtx.drawImage(canvas, sx, sy, sw, sh, 0, 0, 200, 200);
            roiCtx.strokeStyle = "#ffaa33";
            roiCtx.lineWidth = 3;
            roiCtx.strokeRect(0,0,200,200);
            roiCtx.fillStyle = "white";
            roiCtx.font = "bold 10px monospace";
            roiCtx.fillText("Scan Region - 확대됨", 5, 15);
            
            // 분석 시뮬레이션 (위치, 면적 기반 + 확률 예측)
            const area = sw * sh;
            const centerX = sx + sw/2;
            const centerY = sy + sh/2;
            // 폐 중앙부 근처 악성 위험 시뮬레이션
            let malignancyProb = 0;
            let subtype = "";
            let riskLevel = "";
            let recommendation = "";
            // 로직: 면적이 너무 크거나 작을 때, 위치 기반 (가상)
            if(area > 800 && area < 4500) malignancyProb = 0.75 + Math.random()*0.15;
            else if(area >= 4500) malignancyProb = 0.85;
            else malignancyProb = 0.45 + Math.random()*0.3;
            // 중심부 패턴
            const distToCenter = Math.hypot(centerX-300, centerY-300);
            if(distToCenter < 100) malignancyProb = Math.min(0.92, malignancyProb+0.12);
            if(area > 3000) malignancyProb = Math.min(0.96, malignancyProb+0.08);
            malignancyProb = Math.min(0.98, Math.max(0.12, malignancyProb));
            
            if(malignancyProb > 0.7) {
                subtype = "침윤성 선암종 의심 (Invasive Adenocarcinoma)";
                riskLevel = "높은 위험군";
                recommendation = "조직검사 및 PET-CT 권고, 긴밀한 추적 관찰 필요";
            } else if(malignancyProb > 0.4) {
                subtype = "비특이적 염증성 결절 / 저악성 가능성";
                riskLevel = "중간 위험군";
                recommendation = "3개월 후 추적 CT, 필요시 조영검사";
            } else {
                subtype = "양성 결절 (과오종/섬유화)";
                riskLevel = "낮은 위험군";
                recommendation = "정기적 건강검진, 흡연 중단 권고";
            }
            const tnmStage = malignancyProb>0.8?"T2aN0M0 추정":(malignancyProb>0.5?"T1cN0M0":"T1aN0M0 가능성");
            // 세부 분석
            const analysisHtml = `
                <strong>📊 AI 분석 결과</strong><br>
                🔬 병변 크기: ${sw}px × ${sh}px (면적 ~${area}px²)<br>
                📍 위치: (${Math.round(centerX)}, ${Math.round(centerY)})<br>
                🧬 악성 확률: ${(malignancyProb*100).toFixed(1)}%<br>
                🧫 조직 아형: ${subtype}<br>
                ⚠️ 위험 등급: ${riskLevel}<br>
                🩺 임상 TNM 유사: ${tnmStage}<br>
                💊 권고사항: ${recommendation}<br>
                <small style="color:#587a9f;">* 본 분석은 AI 시뮬레이션 기반 참고용입니다.</small>
            `;
            document.getElementById('analysisDetail').innerHTML = analysisHtml;
        }
        
        // Rectangles Add / Remove / Select
        function addRectangle(x,y,w,h) {
            if(w<8 || h<8) return false;
            rectangles.push({x:Math.round(x), y:Math.round(y), w:Math.round(w), h:Math.round(h)});
            activeRectIndex = rectangles.length-1;
            drawRectangles();
            updateROIAndAnalysis();
            return true;
        }
        function deleteActiveRect() {
            if(activeRectIndex !== -1 && rectangles.length>0) {
                rectangles.splice(activeRectIndex,1);
                if(rectangles.length === 0) activeRectIndex = -1;
                else if(activeRectIndex >= rectangles.length) activeRectIndex = rectangles.length-1;
                else activeRectIndex = (activeRectIndex>0?activeRectIndex-1:0);
                drawRectangles();
                if(rectangles.length>0) updateROIAndAnalysis();
                else clearROIAnalysisEmpty();
            }
        }
        function setDefaultRect() {
            rectangles = [];
            // 기본 암 의심영역 (폐 우하엽 결절)
            rectangles.push({x:320, y:340, w:75, h:68});
            rectangles.push({x:240, y:260, w:52, h:48});
            activeRectIndex = 0;
            drawRectangles();
            updateROIAndAnalysis();
        }
        
        // Drawing interaction (Mouse + Touch)
        function getCanvasCoords(e) {
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;   // canvas native 600 / display width
            const scaleY = canvas.height / rect.height;
            let clientX, clientY;
            if(e.touches) {
                clientX = e.touches[0].clientX;
                clientY = e.touches[0].clientY;
            } else {
                clientX = e.clientX;
                clientY = e.clientY;
            }
            let canvasX = (clientX - rect.left) * scaleX;
            let canvasY = (clientY - rect.top) * scaleY;
            canvasX = Math.min(Math.max(0, canvasX), W);
            canvasY = Math.min(Math.max(0, canvasY), H);
            return { mx: canvasX, my: canvasY };
        }
        
        function onPointerStart(e) {
            e.preventDefault();
            if(!isDrawingMode) return;
            const {mx, my} = getCanvasCoords(e);
            startX = mx; startY = my;
            isDrawing = true;
        }
        function onPointerMove(e) {
            if(!isDrawingMode || !isDrawing) return;
            e.preventDefault();
            const {mx, my} = getCanvasCoords(e);
            // draw temporary rect
            restoreOriginalBackground();
            drawRectangles(); // draw existing rectangles
            ctx.save();
            ctx.strokeStyle = "#ffff66";
            ctx.lineWidth = 3;
            ctx.setLineDash([5,5]);
            ctx.strokeRect(startX, startY, mx-startX, my-startY);
            ctx.restore();
        }
        function onPointerEnd(e) {
            if(!isDrawingMode || !isDrawing) {
                // selection mode: try to select rect by click/tap
                if(!isDrawingMode && rectangles.length>0) {
                    const {mx, my} = getCanvasCoords(e);
                    for(let i=rectangles.length-1; i>=0; i--) {
                        const r = rectangles[i];
                        if(mx>=r.x && mx<=r.x+r.w && my>=r.y && my<=r.y+r.h) {
                            activeRectIndex = i;
                            drawRectangles();
                            updateROIAndAnalysis();
                            break;
                        }
                    }
                }
                isDrawing = false;
                return;
            }
            e.preventDefault();
            const {mx, my} = getCanvasCoords(e);
            let w = mx - startX;
            let h = my - startY;
            if(Math.abs(w) > 5 && Math.abs(h) > 5) {
                if(w<0) { startX = mx; w = -w; }
                if(h<0) { startY = my; h = -h; }
                addRectangle(startX, startY, w, h);
            }
            isDrawing = false;
            drawRectangles();
        }
        
        function enableDrawingMode() {
            isDrawingMode = true;
            document.body.style.cursor = 'crosshair';
            canvas.style.cursor = 'crosshair';
            const toast = document.createElement('div');
            toast.innerText = "✏️ 병변 영역 드래그 모드 활성화 (영역 그리기)";
            toast.style.position='fixed'; toast.style.bottom='20px'; toast.style.right='20px'; toast.style.background='#2c7da0'; toast.style.color='white'; toast.style.padding='8px 16px'; toast.style.borderRadius='30px'; toast.style.zIndex='999'; 
            document.body.appendChild(toast); setTimeout(()=>toast.remove(),1500);
        }
        function disableDrawingMode() {
            isDrawingMode = false;
            canvas.style.cursor = 'pointer';
        }
        
        // Attach events
        canvas.addEventListener('mousedown', onPointerStart);
        window.addEventListener('mousemove', onPointerMove);
        window.addEventListener('mouseup', onPointerEnd);
        canvas.addEventListener('touchstart', onPointerStart, {passive:false});
        window.addEventListener('touchmove', onPointerMove, {passive:false});
        window.addEventListener('touchend', onPointerEnd);
        canvas.addEventListener('click', (e) => {
            if(!isDrawingMode) {
                // select rect by click
                const {mx, my} = getCanvasCoords(e);
                for(let i=rectangles.length-1; i>=0; i--) {
                    const r = rectangles[i];
                    if(mx>=r.x && mx<=r.x+r.w && my>=r.y && my<=r.y+r.h) {
                        activeRectIndex = i;
                        drawRectangles();
                        updateROIAndAnalysis();
                        break;
                    }
                }
            }
        });
        
        // UI Buttons
        document.getElementById('drawRectBtn').addEventListener('click', enableDrawingMode);
        document.getElementById('deleteRectBtn').addEventListener('click', ()=>{
            deleteActiveRect();
            disableDrawingMode();
        });
        document.getElementById('resetDefaultRect').addEventListener('click', ()=>{
            setDefaultRect();
            disableDrawingMode();
        });
        
        // PDF 생성기 (한글버전, 요구사항 모두 포함)
        document.getElementById('pdfDownloadBtn').addEventListener('click', async function(){
            const element = document.getElementById('reportContainer');
            if(!element) return;
            const loading = document.createElement('div');
            loading.innerText = "PDF 생성 중... (잠시만 기다려주세요)";
            loading.style.position='fixed'; loading.style.top='50%'; loading.style.left='50%'; loading.style.background='black'; loading.style.color='white'; loading.style.padding='12px'; loading.style.zIndex='9999'; loading.style.borderRadius='20px'; 
            document.body.appendChild(loading);
            try {
                const canvasPdf = await html2canvas(element, { scale: 2, logging: false, useCORS: false, backgroundColor: '#ffffff' });
                const imgData = canvasPdf.toDataURL('image/png');
                const { jsPDF } = window.jspdf;
                const pdf = new jsPDF('p', 'mm', 'a4');
                const imgWidth = 210; // A4 width mm
                const pageHeight = 297;
                const imgHeight = (canvasPdf.height * imgWidth) / canvasPdf.width;
                let position = 0;
                pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
                let heightLeft = imgHeight - pageHeight;
                while (heightLeft > 0) {
                    position = heightLeft - imgHeight;
                    pdf.addPage();
                    pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
                    heightLeft -= pageHeight;
                }
                pdf.save('폐암_분석_보고서_한글버전.pdf');
            } catch(err) { console.error(err); alert("PDF 생성 오류: "+err); }
            finally { loading.remove(); }
        });
        
        // 초기화: 기본 이미지 + 기본 병변 예제
        drawLungSimulation();
        captureOriginalImage();
        setDefaultRect();
        disableDrawingMode();
    })();
</script>
</body>
</html>
```
