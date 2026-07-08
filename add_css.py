import sys

css = """
    /* Photo Album Masonry & Neon Glow Styles */
    .masonry-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 20px;
      align-items: start;
    }
    .photo-card {
      background: rgba(30, 41, 59, 0.7);
      border-radius: 12px;
      overflow: hidden;
      cursor: pointer;
      transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
      position: relative;
      border: 1px solid rgba(255,255,255,0.05);
    }
    .photo-card:hover {
      transform: translateY(-8px);
      box-shadow: 0 15px 30px rgba(0,0,0,0.4);
      z-index: 2;
    }
    
    /* Condition Neon Glows */
    .photo-card[data-condition="good"]:hover {
      box-shadow: 0 15px 30px rgba(0,0,0,0.4), 0 0 20px rgba(16, 185, 129, 0.4);
      border-color: rgba(16, 185, 129, 0.5);
    }
    .photo-card[data-condition="fair"]:hover {
      box-shadow: 0 15px 30px rgba(0,0,0,0.4), 0 0 20px rgba(245, 158, 11, 0.4);
      border-color: rgba(245, 158, 11, 0.5);
    }
    .photo-card[data-condition="critical"]:hover {
      box-shadow: 0 15px 30px rgba(0,0,0,0.4), 0 0 20px rgba(239, 68, 68, 0.4);
      border-color: rgba(239, 68, 68, 0.5);
    }

    .photo-card-img-container {
      width: 100%;
      padding-top: 75%; /* 4:3 Aspect Ratio */
      position: relative;
      overflow: hidden;
      background: #0f172a;
    }
    .photo-card img {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      object-fit: cover;
      transition: transform 0.5s;
    }
    .photo-card:hover img {
      transform: scale(1.05);
    }
    .photo-card-body {
      padding: 16px;
      position: relative;
    }
    .photo-card-title {
      font-weight: 600;
      color: white;
      font-size: 16px;
      margin-bottom: 4px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .photo-card-subtitle {
      color: #94a3b8;
      font-size: 13px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .photo-card-hover-details {
      max-height: 0;
      opacity: 0;
      overflow: hidden;
      transition: all 0.3s ease;
      font-size: 12px;
      color: #cbd5e1;
      margin-top: 0;
    }
    .photo-card:hover .photo-card-hover-details {
      max-height: 60px;
      opacity: 1;
      margin-top: 12px;
      padding-top: 12px;
      border-top: 1px solid rgba(255,255,255,0.1);
    }
    .condition-ring {
      width: 10px; height: 10px; border-radius: 50%;
    }
    .ring-good { background: #10b981; box-shadow: 0 0 8px #10b981; }
    .ring-fair { background: #f59e0b; box-shadow: 0 0 8px #f59e0b; }
    .ring-critical { background: #ef4444; box-shadow: 0 0 8px #ef4444; }
    .ring-unknown { background: #64748b; }
    
    .filmstrip-thumb {
      height: 60px;
      width: 80px;
      object-fit: cover;
      cursor: pointer;
      opacity: 0.6;
      border: 2px solid transparent;
      border-radius: 4px;
      transition: 0.2s;
    }
    .filmstrip-thumb:hover, .filmstrip-thumb.active {
      opacity: 1;
      border-color: #38bdf8;
    }
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

insert_pos = html.find('</style>')
if insert_pos != -1:
    new_html = html[:insert_pos] + css + html[insert_pos:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print('CSS added successfully.')
else:
    print('Error: </style> not found')

