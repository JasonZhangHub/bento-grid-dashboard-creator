# PROMPT V4: For generating multi-slide (3-5) HTML presentations from a PDF. First, the prompt reasons about and breaks down the document into key sections. Then, for each section, it generates a 16:9 HTML presentation slide with summary and bullet points, focusing on conciseness, visual engagement, and key highlights.

# Part 1: Reasoning and Section Breakdown
REASONING_PROMPT = """
You are an AI assistant tasked with reading a PDF document and breaking it down into a concise set of key sections (typically 3-5). 
Your first step is to carefully read and analyze the document, then summarize its overall purpose and main themes. 
Next, identify and list the most important sections or topics that best represent the core content and logical structure of the document. 
For each section, provide a short, punchy title and a 1-sentence summary describing its focus and significance. 
Your output should be a structured list of section titles and summaries, suitable for use as the outline of a slide presentation. 
Be as concise as possible—avoid wordiness and focus on what matters most for a visual presentation.
"""

# Part 2: Slide Generation (Concise, Visually Engaging 16:9 Presentation Slide)
SLIDE_PROMPT = """
You are an AI assistant tasked with creating a visually engaging, concise HTML presentation slide for a given section of a document. 
Each slide must:
- Use a 16:9 aspect ratio, styled as a modern presentation slide.
- Be highly concise: use short phrases, keywords, and visual highlights instead of long sentences.
- Visually emphasize the most important points (e.g., bold, color, icons, or callout boxes).
- If the section contains any key metrics, numbers, or comparisons, display them as a simple chart, infographic, or diagram (e.g., bar, pie, or icon-based visual). Use HTML/CSS/SVG for visuals—do not use images.
- Layout can be flexible: allow for side-by-side blocks, split sections, or visual callouts, as long as the slide remains 16:9 and visually balanced.
- Include a clear, prominent section title.
- Use 3-5 key points or highlights (bullets, icons, or callouts). Avoid paragraphs.
- Use whitespace and large text for clarity and impact.
- Ensure the slide is visually engaging and suitable for projection or sharing.

**Reference HTML Structure (flexible, visually engaging):**
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>[Section Title]</title>
  <style>
    body { background: #f4f7fa; margin: 0; padding: 0; }
    .slide-container {
      width: 100vw;
      height: 100vh;
      aspect-ratio: 16/9;
      display: flex;
      align-items: center;
      justify-content: center;
      background: white;
    }
    .slide-content {
      width: 85vw;
      max-width: 1400px;
      height: 48vw;
      max-height: 750px;
      background: #fff;
      border-radius: 28px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.12);
      padding: 48px 60px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 2.5em;
    }
    .slide-title {
      font-size: 2.6em;
      color: #1a237e;
      font-weight: 800;
      margin-bottom: 0.2em;
      letter-spacing: 0.01em;
    }
    .highlights {
      display: flex;
      flex-wrap: wrap;
      gap: 2em;
      margin-bottom: 0.5em;
    }
    .highlight-box {
      background: #e3f2fd;
      border-left: 6px solid #1976d2;
      border-radius: 12px;
      padding: 1.1em 1.5em;
      font-size: 1.25em;
      font-weight: 600;
      color: #0d3056;
      min-width: 220px;
      flex: 1 1 220px;
      display: flex;
      align-items: center;
      gap: 0.7em;
    }
    .highlight-icon {
      font-size: 1.5em;
      margin-right: 0.5em;
    }
    .metrics-row {
      display: flex;
      gap: 2em;
      margin-top: 1.5em;
      justify-content: flex-start;
      align-items: flex-end;
    }
    .metric-chart {
      flex: 1 1 180px;
      min-width: 180px;
      max-width: 320px;
      background: #f1f8e9;
      border-radius: 10px;
      padding: 1.2em 1em 1.5em 1em;
      display: flex;
      flex-direction: column;
      align-items: center;
      box-shadow: 0 2px 8px rgba(60,120,60,0.07);
    }
    .metric-label {
      font-size: 1.1em;
      color: #388e3c;
      font-weight: 700;
      margin-bottom: 0.5em;
    }
    .metric-bar {
      width: 90%;
      height: 22px;
      background: linear-gradient(90deg, #43a047 70%, #c8e6c9 100%);
      border-radius: 8px;
      margin-bottom: 0.5em;
      position: relative;
    }
    .metric-value {
      position: absolute;
      right: 10px;
      top: 0;
      font-size: 1.1em;
      color: #1b5e20;
      font-weight: 700;
    }
    /* Responsive adjustments */
    @media (max-width: 1000px) {
      .slide-content { padding: 18px 2vw; }
      .slide-title { font-size: 1.5em; }
      .highlight-box { font-size: 1em; }
    }
    @media (max-width: 700px) {
      .slide-content { padding: 8px 1vw; }
      .slide-title { font-size: 1.1em; }
      .highlight-box { font-size: 0.9em; }
    }
  </style>
</head>
<body>
  <div class=\"slide-container\">
    <div class=\"slide-content\">
      <div class=\"slide-title\">[Section Title]</div>
      <div class=\"highlights\">
        <div class=\"highlight-box\"><span class=\"highlight-icon\">💡</span>[Key Point 1]</div>
        <div class=\"highlight-box\"><span class=\"highlight-icon\">⭐</span>[Key Point 2]</div>
        <div class=\"highlight-box\"><span class=\"highlight-icon\">🔥</span>[Key Point 3]</div>
        <!-- Add more highlight-boxes as needed -->
      </div>
      <div class=\"metrics-row\">
        <!-- Example metric chart (bar, pie, or icon-based) -->
        <div class=\"metric-chart\">
          <div class=\"metric-label\">[Metric Label]</div>
          <div class=\"metric-bar\"><span class=\"metric-value\">[Value]</span></div>
        </div>
        <!-- Add more metric-charts as needed -->
      </div>
    </div>
  </div>
</body>
</html>
""" 