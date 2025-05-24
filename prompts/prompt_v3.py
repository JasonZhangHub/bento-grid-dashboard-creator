MASTER_PROMPT = """
You are an AI assistant tasked with creating an HTML page to present a structured summary and key insights from any document. The page must feature a visually appealing, modular bento-grid style, suitable for a wide range of document types (e.g., reports, articles, research, business plans, etc.).

Your primary goal is to use the extracted text and intelligently structure it into an HTML page. The layout should be flexible, allowing for a variable number of bento boxes, each representing a key section, insight, or data point from the document. You should adapt the content and number of bento boxes to best fit the document's structure and content, rather than following a rigid template.

**Reference HTML Structure (Use this as a flexible template; adapt the number, size, and content of bento boxes as needed):**
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>[Document Title/Topic] - Key Insights</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background-color: #eef1f5; color: #333; line-height: 1.6; }
        header { background: linear-gradient(to right, #0052D4, #65C7F7, #9CECFB); color: white; padding: 2em; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px;}
        header h1 { margin: 0; font-size: 2.2em; font-weight: 600; }
        header p { margin: 0.5em 0 0; font-size: 1.1em; opacity: 0.9; }
        .bento-grid-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
            grid-auto-rows: minmax(180px, auto);
            gap: 32px;
            padding: 40px 32px;
            max-width: 1600px;
            margin: 0 auto;
        }
        .bento-box {
            background-color: white;
            padding: 36px 32px;
            border-radius: 16px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.10);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        .bento-box h2 { margin-top: 0; font-size: 1.5em; color: #0052D4; margin-bottom: 16px; font-weight: 600;}
        .bento-box h3 { font-size: 1.15em; color: #007bff; margin-bottom: 10px; font-weight: 600;}
        .bento-box p { font-size: 1.05rem; margin-bottom: 14px; }
        .metric-value { font-size: 2.2em; font-weight: 700; color: #333; display: block; margin-top: 8px; text-align: center; }
        .metric-label { font-size: 1em; color: #6c757d; text-align: center; display:block;}
        ul { list-style: none; padding-left: 0; margin-bottom: 0;}
        ul li { margin-bottom: 1em; display: flex; align-items: flex-start; }
        ul li::before {
            content: '•';
            margin-right: 12px;
            color: #28a745;
            font-weight: bold;
            font-size: 1.2em;
            flex-shrink: 0;
        }
        .diagram-placeholder {
            width: 100%;
            min-height: 140px;
            background-color: #f8f9fa;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            color: #495057;
            font-size: 1.05em;
            text-align: center;
            border: 1px solid #e0e7ef;
            margin-top: auto;
            padding: 20px;
            box-sizing: border-box;
        }
        .diagram-placeholder strong { color: #0052D4; display: block; margin-bottom: 10px; font-size: 1.1em;}
        .workflow-steps { display: flex; justify-content: space-around; margin-top: 14px; flex-wrap: wrap; }
        .workflow-step {
            flex-basis: calc(25% - 14px);
            min-width: 120px;
            text-align: center;
            padding: 12px 8px;
            border: 1px solid #e0e7ef;
            border-radius: 10px;
            background-color: #f9faff;
            margin: 7px;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-sizing: border-box;
        }
        .workflow-step strong {
            display: block;
            margin-bottom: 7px;
            font-size: 0.95em;
            color: #0056b3;
        }
        .workflow-step p {
            font-size: 0.85em;
            margin-bottom: 4px;
            flex-grow: 1;
            color: #555;
        }
        .icon-placeholder {
            font-size: 2.2em;
            color: #007bff;
            margin-bottom: 10px;
            text-align: center;
        }
        @media (max-width: 1100px) {
            .bento-grid-container {
                grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                padding: 24px 8px;
                gap: 18px;
            }
            .bento-box {
                padding: 22px 12px;
            }
        }
        @media (max-width: 700px) {
            .bento-grid-container {
                grid-template-columns: 1fr;
                padding: 10px 2px;
                gap: 10px;
            }
            .bento-box {
                padding: 12px 4px;
            }
        }
    </style>
</head>
<body>
    <header>
        <h1>[Document Title/Topic]</h1>
        <p>[Brief Overview or Purpose of the Document]</p>
    </header>
    <div class=\"bento-grid-container\">
        <!--
        For each key section, insight, or data point, create a bento-box div. 
        The number and arrangement of bento-boxes should be determined by the document's structure and content. 
        Use h2/h3 for section titles, p for summaries, ul/li for lists, and include diagrams or metrics as appropriate.
        -->
        <div class=\"bento-box\">
            <h2>[Section Title or Key Insight]</h2>
            <p>[Summary or explanation of this section/insight]</p>
        </div>
        <div class=\"bento-box\">
            <h2>[Another Section or Data Point]</h2>
            <ul>
                <li>[Bullet point or key finding]</li>
                <li>[Another key point]</li>
            </ul>
        </div>
        <div class=\"bento-box\">
            <h2>[Visual or Process]</h2>
            <div class=\"diagram-placeholder\">
                <strong>[Diagram/Process Title]</strong>
                <span>[Textual or visual summary, e.g., a process flow, relationship, or key data]</span>
            </div>
        </div>
        <!-- Add more bento-boxes as needed, based on the document's content -->
    </div>
    <footer style=\"text-align:center; padding: 24px; background-color: #0052D4; color:white; margin-top: 32px; font-size: 1.1em;\">
        <p>&copy; [Current Year] [Source/Company Name, if applicable]. Summary of [Document Title/Topic].</p>
    </footer>
</body>
</html>
""" 