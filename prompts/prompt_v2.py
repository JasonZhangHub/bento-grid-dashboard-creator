MASTER_PROMPT = """
You are an AI assistant tasked with creating an HTML page to present a structured summary and key insights from a document. The page must feature a visually appealing bento-grid style, similar to a modern dashboard layout. You will be provided with extracted text from a PDF document containing all necessary information to be summarized.
 
Your primary goal is to meticulously use this extracted text and intelligently structure it into an HTML page. This page should closely mirror the layout, style, and component structure of the Reference HTML Structure provided below. You must adapt the content from the provided text to populate the bento-grid components effectively, highlighting key information, main arguments, important data points, processes, or other significant takeaways. You will need to make informed decisions on how to best represent the document's core content within the bento box framework.

**Reference HTML Structure (Use this as a template for style and layout; adapt placeholder text based on the input document's content)**:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Document Title/Topic] - Key Insights</title>
    <style>
        /* Basic styling for demonstration - EXPAND SIGNIFICANTLY for a production page */
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background-color: #eef1f5; color: #333; line-height: 1.6; }
        header { background: linear-gradient(to right, #0052D4, #65C7F7, #9CECFB); /* ADAPT GRADIENT COLORS TO DOCUMENT THEME/BRANDING if applicable */ color: white; padding: 2em; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px;}
        header h1 { margin: 0; font-size: 2.2em; font-weight: 600; }
        header p { margin: 0.5em 0 0; font-size: 1.1em; opacity: 0.9; }

        .bento-grid-container {
            display: grid;
            grid-template-columns: repeat(4, 1fr); /* 4 columns */
            grid-auto-rows: minmax(150px, auto);
            gap: 20px;
            padding: 25px;
            max-width: 1400px;
            margin: 0 auto;
        }
        .bento-box {
            background-color: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        /* Spanning classes */
        .col-span-1 { grid-column: span 1; }
        .col-span-2 { grid-column: span 2; }
        .col-span-3 { grid-column: span 3; }
        .col-span-4 { grid-column: span 4; }
        .row-span-1 { grid-row: span 1; }
        .row-span-2 { grid-row: span 2; }

        .bento-box h2 { margin-top: 0; font-size: 1.4em; color: #0052D4; /* ADAPT COLOR TO DOCUMENT THEME/BRANDING if applicable */ margin-bottom: 15px; font-weight: 600;}
        .bento-box h3 { font-size: 1.1em; color: #007bff; /* ADAPT COLOR TO DOCUMENT THEME/BRANDING if applicable */ margin-bottom: 8px; font-weight: 600;}
        .bento-box p { font-size: 0.9rem; margin-bottom: 10px; }
        .metric-value { font-size: 2.2em; font-weight: 700; color: #333; /* ADAPT COLOR TO DOCUMENT THEME/BRANDING if applicable */ display: block; margin-top: 5px; text-align: center; }
        .metric-label { font-size: 0.9em; color: #6c757d; text-align: center; display:block;}

        ul { list-style: none; padding-left: 0; margin-bottom: 0;}
        ul li { margin-bottom: 0.8em; display: flex; align-items: flex-start; }
        ul li::before {
            content: '✓'; /* Checkmark icon, or adapt (e.g., '•', '→') based on context */
            margin-right: 10px;
            color: #28a745; /* Green color for checkmark, adapt as needed */
            font-weight: bold;
            font-size: 1.1em;
            flex-shrink: 0;
        }

        .diagram-placeholder {
            width: 100%;
            min-height: 180px;
            background-color: #f8f9fa;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            color: #495057;
            font-size: 0.9em;
            text-align: center;
            border: 1px solid #e0e7ef;
            margin-top: auto;
            padding: 15px;
            box-sizing: border-box;
        }
        .diagram-placeholder strong { color: #0052D4; /* ADAPT COLOR TO DOCUMENT THEME/BRANDING if applicable */ display: block; margin-bottom: 8px; font-size: 1em;}

        .workflow-steps { display: flex; justify-content: space-around; margin-top: 10px; flex-wrap: wrap; }
        .workflow-step {
            flex-basis: calc(20% - 10px); /* Assumes 5 steps. Adjust if different (e.g., calc(25% - 10px) for 4 steps, calc(16.66% - 10px) for 6 steps) */
            min-width: 80px; /* Adjust if text is longer, but aim for very concise text */
            text-align: center;
            padding: 8px 4px;
            border: 1px solid #e0e7ef;
            border-radius: 8px;
            background-color: #f9faff;
            margin: 5px;
            display: flex;
            flex-direction: column;
            align-items: center;
            box-sizing: border-box;
        }
        /* Specific adjustment for a different number of items in a row, e.g., 4 items */
        .workflow-steps.four-items .workflow-step {
            flex-basis: calc(25% - 10px);
            min-width: 110px; /* Can be slightly wider if fewer items */
        }
        /* Specific adjustment for 6 items in a row */
         .workflow-steps.six-items .workflow-step {
            flex-basis: calc(16.66% - 10px);
            min-width: 70px; /* Must be very narrow */
        }

        .workflow-step strong {
            display: block;
            margin-bottom: 5px;
            font-size: 0.75em; /* Keep text concise */
            color: #0056b3; /* ADAPT COLOR TO DOCUMENT THEME/BRANDING if applicable */
        }
        .workflow-step p {
            font-size: 0.68em; /* Keep text very concise */
            margin-bottom: 3px;
            flex-grow: 1;
            color: #555;
        }
        .workflow-step small {
            font-size: 0.65em; /* Keep text concise */
            color: #007bff; /* ADAPT COLOR TO DOCUMENT THEME/BRANDING if applicable */
        }
        .workflow-step .step-number {
            background-color: #007bff; /* ADAPT COLOR TO DOCUMENT THEME/BRANDING if applicable */
            color: white;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-bottom: 8px;
            font-size: 0.75em;
        }

        .icon-placeholder {
            font-size: 2em;
            color: #007bff; /* ADAPT COLOR TO DOCUMENT THEME/BRANDING if applicable */
            margin-bottom: 8px;
            text-align: center;
        }

        .value-proposition-section { margin-bottom: 15px; } /* Can be used for any list of key points/arguments */
        .value-proposition-section:last-child { margin-bottom: 0; }

        .kpi-box { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align:center; flex-grow: 1;}
        .kpi-box .icon-placeholder { font-size: 2.5em; margin-bottom: 10px;}
        .kpi-box p.description { font-size: 0.9rem; margin-bottom:15px; } /* Optional description for KPI/Data Point boxes */
        .kpi-box .metric-value { font-size: 2.8em; color: #007bff; /* ADAPT COLOR TO DOCUMENT THEME/BRANDING if applicable */ margin-bottom: 0px;}
        .kpi-box .metric-label { font-size: 0.85em; color: #555; margin-top:0px;}
    </style>
</head>
<body>
    <header>
        <h1>Key Insights: [Document Title/Topic]</h1>
        <p>[Brief Overview or Purpose of the Document - Keep it concise and informative]</p>
    </header>
    <div class="bento-grid-container">
        <div class="bento-box col-span-2 row-span-1">
            <h2>Overview of [Document Topic/Main Section]</h2>
            <p>[Extract and adapt the general introduction, abstract, or a key opening section from the document. What is the core message or purpose? What are the main points discussed? Make it informative and engaging.]</p>
        </div>
        <div class="bento-box col-span-1 row-span-1 kpi-box">
            <h2>[Key Data Point/Statistic Title 1 - e.g., "Growth Rate"]</h2>
            <div class="icon-placeholder">[Relevant Icon Placeholder e.g., 📊, 📈, 📉, 🎯, 💡]</div>
            <span class="metric-value">[Specific Numeric Value from Document]</span>
            <span class="metric-label">[Brief Label for the Data Point/Statistic]</span>
        </div>
        <div class="bento-box col-span-1 row-span-1 kpi-box">
             <h2>[Key Data Point/Statistic Title 2 - e.g., "User Engagement"]</h2>
            <div class="icon-placeholder">[Relevant Icon Placeholder]</div>
            <span class="metric-value">[Specific Numeric Value from Document]</span>
            <span class="metric-label">[Brief Label for the Data Point/Statistic]</span>
        </div>
        <div class="bento-box col-span-4 row-span-2">
            <h2>[Title: e.g., "Main Arguments & Themes" or "Key Sections Summarized"]</h2>
            <div class="value-proposition-section"> <h3>[Key Theme/Argument/Section Title 1 - Clear and Concise]</h3>
                <p>[Concise summary or explanation of this theme/argument/section, extracted and synthesized from the document.]</p>
            </div>
            <div class="value-proposition-section">
                <h3>[Key Theme/Argument/Section Title 2]</h3>
                <p>[Concise summary or explanation of this theme/argument/section.]</p>
            </div>
            <div class="value-proposition-section">
                <h3>[Key Theme/Argument/Section Title 3]</h3>
                <p>[Concise summary or explanation of this theme/argument/section.]</p>
            </div>
            <div class="value-proposition-section">
                <h3>[Key Theme/Argument/Section Title 4 - e.g., "Critical Findings" or "Important Implications"]</h3>
                <p>[Concise summary or explanation of this theme/argument/section.]</p>
            </div>
        </div>
        <div class="bento-box col-span-4 row-span-1">
            <h2>[Title for this section: e.g., "Key Processes Outlined" or "Core Concepts at a Glance" or "Methodology Steps"]</h2>
            <div class="workflow-steps"> <div class="workflow-step">
                    <div class="step-number">[1]</div><strong>[Step/Concept/Component 1 Title from Document]</strong>
                    <p>[EXTREMELY BRIEF description of step/concept 1.]</p>
                    <small>[Optional: Related detail - VERY BRIEF]</small>
                </div>
                <div class="workflow-step">
                    <div class="step-number">[2]</div><strong>[Step/Concept/Component 2 Title from Document]</strong>
                    <p>[EXTREMELY BRIEF description of step/concept 2.]</p>
                    <small>[Optional: Related detail - VERY BRIEF]</small>
                </div>
                <div class="workflow-step">
                    <div class="step-number">[3]</div><strong>[Step/Concept/Component 3 Title from Document]</strong>
                    <p>[EXTREMELY BRIEF description of step/concept 3.]</p>
                    <small>[Optional: Related detail - VERY BRIEF]</small>
                </div>
                </div>
        </div>
        <div class="bento-box col-span-2 row-span-2">
            <h2>[Title: e.g., "Key Findings & Highlights" or "Important Details" or "Supporting Evidence"]</h2>
            <ul>
                <li>[Finding/Highlight/Detail 1 from Document - Summarize concisely]</li>
                <li>[Finding/Highlight/Detail 2 from Document - Summarize concisely]</li>
                <li>[Finding/Highlight/Detail 3 from Document - Summarize concisely]</li>
                <li>[Finding/Highlight/Detail 4 from Document - Summarize concisely]</li>
                <li>[Finding/Highlight/Detail 5 from Document - Summarize concisely]</li>
            </ul>
        </div>
        <div class="bento-box col-span-2 row-span-2">
            <h2>[Title: e.g., "Visualized Concept" or "Context & Implications" or "Data Overview"]</h2>
            <div class="diagram-placeholder">
                <strong>[Sub-heading for diagram/info - e.g., "Simplified Process Flow" or "Key Relationships" or "Core Principles"]</strong>
                <span>[Textual representation of a simple flow, relationship, key components, or core principles discussed in the document. Extract and simplify for clarity. This could also be a list of key definitions or a small table if appropriate.]</span>
            </div>
            <p style="font-size:0.9em; text-align:center; margin-top:10px;">[Optional: A brief concluding sentence about the information presented, its significance, or related context from the document.]</p>
        </div>
        <div class="bento-box col-span-4 row-span-1">
            <h2>[Title: e.g., "Underlying Principles" or "Methodology Summary" or "Conclusion Highlights"]</h2>
            <p style="text-align:center; font-size:0.9rem; margin-bottom:12px;">[Brief introductory sentence about these principles, methods, or conclusions. Extract from relevant sections of the document.]</p>
            <div class="workflow-steps"> <div class="workflow-step"><strong>[Principle/Stage/Point 1 Title]</strong><p>[EXTREMELY BRIEF description.]</p></div>
                <div class="workflow-step"><strong>[Principle/Stage/Point 2 Title]</strong><p>[EXTREMELY BRIEF description.]</p></div>
                <div class="workflow-step"><strong>[Principle/Stage/Point 3 Title]</strong><p>[EXTREMELY BRIEF description.]</p></div>
                </div>
        </div>
    </div>
    <footer style="text-align:center; padding: 20px; background-color: #0052D4; /* ADAPT COLOR TO DOCUMENT THEME/BRANDING if applicable */ color:white; margin-top: 20px;">
        <p>&copy; [Current Month] [Current Year] [Source/Company Name, if applicable]. Summary of [Document Title/Topic].</p>
    </footer>
</body>
</html>
"""

SYSTEM_PROMPT = '''
You are an AI assistant tasked with creating an HTML page for a company product or program announcement.
The page must feature a visually appealing bento-grid style, similar to a modern dashboard layout.
You will be provided with a PDF document containing all necessary information about the specific product/program being announced.
'''

ASSISTANT_PROMPT = '''
Your primary goal is to meticulously extract key information from this PDF and intelligently structure it into an HTML page. This page should closely mirror the layout, style, and component structure of the Reference HTML Structure provided below. You must adapt the content specifically for the new product/program detailed in the PDF.
Reference HTML Structure (Use this as a template for style and layout):
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>[NEW PRODUCT/PROGRAM NAME] Announcement</title>
        <style>
            /* Basic styling for demonstration - EXPAND SIGNIFICANTLY for a production page */
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background-color: #eef1f5; color: #333; line-height: 1.6; }
            header { background: linear-gradient(to right, #0052D4, #65C7F7, #9CECFB); /* ADAPT GRADIENT COLORS TO NEW BRANDING */ color: white; padding: 2em; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px;}
            header h1 { margin: 0; font-size: 2.2em; font-weight: 600; }
            header p { margin: 0.5em 0 0; font-size: 1.1em; opacity: 0.9; }
    .bento-grid-container {
                display: grid;
                grid-template-columns: repeat(4, 1fr); /* 4 columns */
                grid-auto-rows: minmax(150px, auto);
                gap: 20px;
                padding: 25px;
                max-width: 1400px;
                margin: 0 auto;
            }
            .bento-box {
                background-color: white;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                overflow: hidden;
                display: flex;
                flex-direction: column;
            }
    /* Spanning classes */
            .col-span-1 { grid-column: span 1; }
            .col-span-2 { grid-column: span 2; }
            .col-span-3 { grid-column: span 3; }
            .col-span-4 { grid-column: span 4; }
            .row-span-1 { grid-row: span 1; }
            .row-span-2 { grid-row: span 2; }
    .bento-box h2 { margin-top: 0; font-size: 1.4em; color: #0052D4; /* ADAPT COLOR TO NEW BRANDING */ margin-bottom: 15px; font-weight: 600;}
            .bento-box h3 { font-size: 1.1em; color: #007bff; /* ADAPT COLOR TO NEW BRANDING */ margin-bottom: 8px; font-weight: 600;}
            .bento-box p { font-size: 0.9rem; margin-bottom: 10px; }
            .metric-value { font-size: 2.2em; font-weight: 700; color: #333; /* ADAPT COLOR TO NEW BRANDING if needed */ display: block; margin-top: 5px; text-align: center; }
            .metric-label { font-size: 0.9em; color: #6c757d; text-align: center; display:block;}
    ul { list-style: none; padding-left: 0; margin-bottom: 0;}
            ul li { margin-bottom: 0.8em; display: flex; align-items: flex-start; }
            ul li::before {
                content: '✓'; /* Checkmark icon */
                margin-right: 10px;
                color: #28a745; /* Green color for checkmark */
                font-weight: bold;
                font-size: 1.1em;
                flex-shrink: 0;
            }
    .diagram-placeholder {
                width: 100%;
                min-height: 180px;
                background-color: #f8f9fa;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                border-radius: 8px;
                color: #495057;
                font-size: 0.9em;
                text-align: center;
                border: 1px solid #e0e7ef;
                margin-top: auto;
                padding: 15px;
                box-sizing: border-box;
            }
            .diagram-placeholder strong { color: #0052D4; /* ADAPT COLOR TO NEW BRANDING */ display: block; margin-bottom: 8px; font-size: 1em;}
    .workflow-steps { display: flex; justify-content: space-around; margin-top: 10px; flex-wrap: wrap; }
            .workflow-step {
                flex-basis: calc(20% - 10px); /* Assumes 5 steps. Adjust if different (e.g., calc(25% - 10px) for 4 steps, calc(16.66% - 10px) for 6 steps) */
                min-width: 80px; /* Adjust if text is longer, but aim for very concise text */
                text-align: center;
                padding: 8px 4px;
                border: 1px solid #e0e7ef;
                border-radius: 8px;
                background-color: #f9faff;
                margin: 5px;
                display: flex;
                flex-direction: column;
                align-items: center;
                box-sizing: border-box;
            }
            /* Specific adjustment for a different number of items in a row, e.g., 4 items */
            .workflow-steps.four-items .workflow-step {
                flex-basis: calc(25% - 10px);
                min-width: 110px; /* Can be slightly wider if fewer items */
            }
            /* Specific adjustment for 6 items in a row */
            .workflow-steps.six-items .workflow-step {
                flex-basis: calc(16.66% - 10px);
                min-width: 70px; /* Must be very narrow */
            }
    .workflow-step strong {
                display: block;
                margin-bottom: 5px;
                font-size: 0.75em; /* Keep text concise */
                color: #0056b3; /* ADAPT COLOR TO NEW BRANDING */
            }
    .workflow-step p {
                font-size: 0.68em; /* Keep text very concise */
                margin-bottom: 3px;
                flex-grow: 1;
                color: #555;
            }
    .workflow-step small {
                font-size: 0.65em; /* Keep text concise */
                color: #007bff; /* ADAPT COLOR TO NEW BRANDING */
            }
    .workflow-step .step-number {
                background-color: #007bff; /* ADAPT COLOR TO NEW BRANDING */
                color: white;
                border-radius: 50%;
                width: 20px;
                height: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                margin-bottom: 8px;
                font-size: 0.75em;
            }
    .icon-placeholder {
                font-size: 2em;
                color: #007bff; /* ADAPT COLOR TO NEW BRANDING */
                margin-bottom: 8px;
                text-align: center;
            }
    .value-proposition-section { margin-bottom: 15px; }
            .value-proposition-section:last-child { margin-bottom: 0; }
    .kpi-box { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align:center; flex-grow: 1;}
            .kpi-box .icon-placeholder { font-size: 2.5em; margin-bottom: 10px;}
            .kpi-box p.description { font-size: 0.9rem; margin-bottom:15px; } /* Optional description for KPI boxes */
            .kpi-box .metric-value { font-size: 2.8em; color: #007bff; /* ADAPT COLOR TO NEW BRANDING */ margin-bottom: 0px;}
            .kpi-box .metric-label { font-size: 0.85em; color: #555; margin-top:0px;}
        </style>
    </head>
    <body>
        <header>
            <h1>Announcing [NEW PRODUCT/PROGRAM NAME]!</h1>
            <p>[Brief Tagline for the New Product/Program - Keep it exciting and informative]</p>
        </header>
    <div class="bento-grid-container">
            <div class="bento-box col-span-2 row-span-1">
                <h2>Introducing [New Product/Program Name]</h2>
                <p>[Extract and adapt the general introduction/overview from the PDF. What is the core purpose? Who benefits? What problem does it solve? Make it engaging for an announcement.]</p>
            </div>
    <div class="bento-box col-span-1 row-span-1 kpi-box">
                <h2>[Key Metric/KPI Title 1 from PDF - e.g., "Pilot Success: Efficiency Boost"]</h2>
                <div class="icon-placeholder">[Relevant Icon Placeholder e.g., 👥, ⏱️, 📈, 🎯, ✨]</div>
                <span class="metric-value">[Specific Metric Value from PDF - e.g., "X%"]</span>
                <span class="metric-label">[Brief Label for Metric from PDF - e.g., "Reduction in X Time"]</span>
            </div>
    <div class="bento-box col-span-1 row-span-1 kpi-box">
                <h2>[Key Metric/KPI Title 2 from PDF - e.g., "Enhanced Engagement"]</h2>
                <div class="icon-placeholder">[Relevant Icon Placeholder]</div>
                <span class="metric-value">[Specific Metric Value from PDF]</span>
                <span class="metric-label">[Brief Label for Metric from PDF]</span>
            </div>
    <div class="bento-box col-span-4 row-span-2">
                <h2>[New Product/Program Name] Value Proposition</h2>
                <div class="value-proposition-section">
                    <h3>[Value Point 1 Title - Clear and Benefit-Oriented]</h3>
                    <p>[Concise description of Value Point 1. Focus on what it means for the user/company.]</p>
                </div>
                <div class="value-proposition-section">
                    <h3>[Value Point 2 Title]</h3>
                    <p>[Concise description of Value Point 2.]</p>
                </div>
                <div class="value-proposition-section">
                    <h3>[Value Point 3 Title]</h3>
                    <p>[Concise description of Value Point 3.]</p>
                </div>
                <div class="value-proposition-section">
                    <h3>[Value Point 4 Title - e.g., "Key Differentiators" or "Strategic Advantage"]</h3>
                    <p>[Concise description of Value Point 4.]</p>
                </div>
            </div>
    <div class="bento-box col-span-4 row-span-1">
                <h2>[Title for this section: e.g., "How [New Product] Streamlines Your Work" or "Core Features at a Glance" or "The [Relevant User] Journey Reimagined"]</h2>
                <div class="workflow-steps"> <div class="workflow-step">
                        <div class="step-number">[1]</div><strong>[Step/Feature 1 Title from PDF]</strong>
                        <p>[EXTREMELY BRIEF description of step/feature 1.]</p>
                        <small>[Optional: Associated tool/module - VERY BRIEF]</small>
                    </div>
                    <div class="workflow-step">
                        <div class="step-number">[2]</div><strong>[Step/Feature 2 Title from PDF]</strong>
                        <p>[EXTREMELY BRIEF description of step/feature 2.]</p>
                        <small>[Optional: Associated tool/module - VERY BRIEF]</small>
                    </div>
                    <div class="workflow-step">
                        <div class="step-number">[3]</div><strong>[Step/Feature 3 Title from PDF]</strong>
                        <p>[EXTREMELY BRIEF description of step/feature 3.]</p>
                        <small>[Optional: Associated tool/module - VERY BRIEF]</small>
                    </div>
                    </div>
            </div>
    <div class="bento-box col-span-2 row-span-2">
                <h2>[Title: e.g., "Key Capabilities & Technologies" or "Under the Hood" or "Highlights & Innovations"]</h2>
                <ul>
                    <li>[Capability/Highlight 1 from PDF]</li>
                    <li>[Capability/Highlight 2 from PDF]</li>
                    <li>[Capability/Highlight 3 from PDF]</li>
                    <li>[Capability/Highlight 4 from PDF]</li>
                    <li>[Capability/Highlight 5 from PDF]</li>
                </ul>
            </div>
            <div class="bento-box col-span-2 row-span-2">
                <h2>[Title: e.g., "The Road Ahead: Future Milestones" or "Technical Insights" or "Data-Driven Approach"]</h2>
                <div class="diagram-placeholder">
                    <strong>[Sub-heading for diagram/info - e.g., "Simplified Architecture Overview" or "Key Rollout Dates" or "Core Data Principles"]</strong>
                    <span>[Textual representation of a simple flow, key dates from a roadmap, or main tech components/principles. Extract from PDF's architecture, future scope, tech stack, or guiding principles sections. Keep it high-level and announcement-appropriate.]</span>
                </div>
                <p style="font-size:0.9em; text-align:center; margin-top:10px;">[Optional: A brief concluding sentence about the technology, future vision, or data security, if relevant and positive.]</p>
            </div>
    <div class="bento-box col-span-4 row-span-1">
                <h2>[Title: e.g., "Our Commitment to Excellence" or "Ensuring Responsible Innovation" or "Continuous Improvement Cycle"]</h2>
                <p style="text-align:center; font-size:0.9rem; margin-bottom:12px;">[Brief introductory sentence about this commitment/process. Extract from PDF's sections on quality, risk mitigation, guiding principles, or improvement cycles.]</p>
                <div class="workflow-steps"> <div class="workflow-step"><strong>[Step 1 Title from PDF process]</strong><p>[EXTREMELY BRIEF description.]</p></div>
                    <div class="workflow-step"><strong>[Step 2 Title from PDF process]</strong><p>[EXTREMELY BRIEF description.]</p></div>
                    <div class="workflow-step"><strong>[Step 3 Title from PDF process]</strong><p>[EXTREMELY BRIEF description.]</p></div>
                    </div>
            </div>
    </div>
        <footer style="text-align:center; padding: 20px; background-color: #0052D4; /* ADAPT COLOR TO NEW BRANDING */ color:white; margin-top: 20px;">
            <p>&copy; [Current Month] [Current Year] [Your Company Name]. [New Product/Program Name] - Internal Announcement.</p>
        </footer>
    </body>
    </html>
 
    Detailed Instructions for the AI Using This Prompt:
        1. Primary Goal: Your objective is to generate a complete and accurate HTML page for a company announcement, based on information from a newly provided PDF document.
        2. Adherence to Template: The Reference HTML Structure above is your blueprint. You must strictly follow its structural organization (divs, classes, bento-box layout) and apply the embedded CSS.
        3. Content Extraction & Adaptation:
            ○ Carefully read the new PDF to identify key information: product/program name, tagline, overview, problem statement, solution, business impact, KPIs (especially pilot results or expected outcomes), core features, user workflows, technical highlights, future milestones, and any guiding principles or commitments.
            ○ Populate all placeholder sections (e.g., [NEW PRODUCT/PROGRAM NAME], [Value Point 1 Title]) with content derived specifically from the new PDF.
            ○ Tone: Maintain an enthusiastic, positive, and professional tone suitable for a company announcement. Focus on benefits and impact.
            ○ Conciseness: Ensure all extracted and adapted text is brief and to the point. Avoid lengthy paragraphs. Bullet points and short phrases are preferred within the bento boxes. For .workflow-step elements, text within <strong> and <p> tags MUST BE EXTREMELY BRIEF to ensure all items fit on a single visual row, especially when there are 4 or more steps.
        4. Branding Customization:
            ○ Locate all CSS comments marked /* ADAPT COLOR TO NEW BRANDING */.
            ○ If the new PDF provides clear branding guidelines or uses distinct colors, adapt these CSS color properties accordingly. If no specific branding is evident, use sensible, professional default colors or retain the template's colors if they are neutral.
        5. Icon Placeholders:
            ○ Retain the icon-placeholder divs.
            ○ Where appropriate, you may suggest relevant Unicode characters as placeholders for icons (e.g., 🚀 for launch, 🎯 for target, 💡 for innovation, 📈 for growth, ⏱️ for efficiency, 👥 for users, ✨ for new features).
        6. Structural Integrity & Workflow Steps:
            ○ The number of .workflow-step divs in Row 3 and Row 5 should match the logical number of steps/features/principles extracted from the PDF (typically 3-6).
            ○ Crucially, if the number of items in a .workflow-steps div is not 5, you MUST add an appropriate helper class to the .workflow-steps div itself (e.g., class="workflow-steps four-items" for 4 items, class="workflow-steps six-items" for 6 items). This will apply the correct flex-basis and min-width from the CSS to help maintain a single-row layout.
            ○ If the PDF outlines a process with more than 6 very brief steps that must be shown, consider if they can be grouped or if a different visualization approach (not covered by this template) would be better. For this template, aim for 3-6 steps per .workflow-steps section.
        7. KPI Boxes (Row 1):
            ○ If the PDF does not provide two distinct, quantifiable KPIs suitable for the top-right boxes, adapt these boxes to showcase other key achievements, highly impactful statements from the PDF, or critical launch information. The goal is to have two compelling, concise pieces of information in these slots.
        8. No External References: Do not include any comments or annotations in the final HTML output that refer back to page numbers or sections of the source PDF (e.g., "Based on PDF page X").
        9. Footer Information: Accurately update the [Current Month], [Current Year], [Your Company Name], and [New Product/Program Name] in the footer. Use the actual current month and year.
        10. Final Output: Deliver the complete, runnable HTML code as a single block, ready to be saved as an .html file. Ensure all tags are correctly opened and closed.
'''
