import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# New HTML for panel-photos
new_panel = """
  <!-- PHOTOS PANEL -->
  <div class="panel" id="panel-photos" style="padding: 0; display: none; height: 100vh; overflow: hidden;">
    
    <!-- Top Filter Bar -->
    <div style="background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(10px); border-bottom: 1px solid rgba(255,255,255,0.1); padding: 16px 24px; position: sticky; top: 0; z-index: 10;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        <div>
          <h2 style="margin: 0; font-size: 24px; font-weight: 600; color: white;">Structure Photo Gallery</h2>
          <div style="color: #94a3b8; font-size: 13px; margin-top: 4px;">Sourced locally from G:\\ Drive repository</div>
        </div>
        
        <!-- Search and Quick Filters -->
        <div style="display: flex; gap: 12px; align-items: center;">
          <input type="text" id="photoGallerySearch" placeholder="Search ID, Road, or District..." style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); color: white; padding: 8px 16px; border-radius: 20px; outline: none; width: 250px;">
          
          <select id="photoFilterType" style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); color: white; padding: 8px 16px; border-radius: 20px; outline: none;">
            <option value="all">All Structures</option>
            <option value="bridges">Bridges</option>
            <option value="culverts">Major Culverts</option>
          </select>
          
          <select id="photoFilterCondition" style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); color: white; padding: 8px 16px; border-radius: 20px; outline: none;">
            <option value="all">Any Condition</option>
            <option value="critical">Critical / Poor</option>
            <option value="fair">Fair</option>
            <option value="good">Good</option>
          </select>
        </div>
      </div>
      
      <!-- Condition Heatmap Strip -->
      <div id="photoHeatmap" style="height: 4px; width: 100%; border-radius: 2px; display: flex; overflow: hidden; background: #333;">
        <!-- Filled dynamically -->
      </div>
    </div>

    <!-- Masonry Grid Container -->
    <div id="photoMasonryContainer" style="padding: 24px; height: calc(100vh - 110px); overflow-y: auto;">
        
        <!-- Pinned Critical Section (Optional, injected via JS if active) -->
        <div id="photoPinnedCritical" style="display: none; margin-bottom: 32px;">
            <h3 style="color: #ef4444; border-bottom: 1px solid rgba(239, 68, 68, 0.3); padding-bottom: 8px; margin-bottom: 16px;">Critical Structures</h3>
            <div id="photoPinnedGrid" class="masonry-grid"></div>
        </div>

        <div id="photoMainGrid" class="masonry-grid">
            <!-- Cards injected here -->
        </div>
    </div>

    <!-- Fullscreen Lightbox -->
    <div id="photoLightbox" style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.95); z-index: 9999; backdrop-filter: blur(5px); flex-direction: row;">
      
      <!-- Left: Image Viewer -->
      <div style="flex-grow: 1; position: relative; display: flex; flex-direction: column;">
        <button id="lightboxClose" style="position: absolute; top: 20px; right: 20px; background: none; border: none; color: white; font-size: 32px; cursor: pointer; z-index: 10;">&times;</button>
        
        <div style="flex-grow: 1; display: flex; align-items: center; justify-content: center; position: relative;">
          <button id="lightboxPrev" style="position: absolute; left: 20px; background: rgba(255,255,255,0.1); border: none; color: white; padding: 16px; border-radius: 50%; cursor: pointer; transition: 0.2s;">&#10094;</button>
          
          <img id="lightboxImage" src="" style="max-width: 90%; max-height: 80vh; object-fit: contain; box-shadow: 0 10px 30px rgba(0,0,0,0.5); transition: transform 0.3s ease;">
          
          <button id="lightboxNext" style="position: absolute; right: 20px; background: rgba(255,255,255,0.1); border: none; color: white; padding: 16px; border-radius: 50%; cursor: pointer; transition: 0.2s;">&#10095;</button>
        </div>
        
        <!-- Filmstrip -->
        <div id="lightboxFilmstrip" style="height: 100px; background: rgba(0,0,0,0.5); display: flex; gap: 8px; padding: 12px; overflow-x: auto; align-items: center; justify-content: center;">
          <!-- Thumbs injected here -->
        </div>
      </div>

      <!-- Right: Metadata Panel -->
      <div style="width: 380px; background: #0f172a; border-left: 1px solid rgba(255,255,255,0.1); display: flex; flex-direction: column; overflow-y: auto;">
        <div style="padding: 24px;">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
            <h2 id="lightboxTitle" style="margin: 0; color: white; font-size: 24px;">Bridge Name</h2>
            <div id="lightboxConditionRing" style="width: 40px; height: 40px; border-radius: 50%; border: 3px solid #10b981; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 14px;">1</div>
          </div>
          
          <div id="lightboxSubtitle" style="color: #94a3b8; font-size: 14px; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.1);">B001 • Kampala District</div>

          <!-- Attributes Grid -->
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px;">
            <div>
              <div style="color: #64748b; font-size: 11px; text-transform: uppercase;">Span / Diameter</div>
              <div id="lightboxSpan" style="color: white; font-size: 14px; font-weight: 500;">-</div>
            </div>
            <div>
              <div style="color: #64748b; font-size: 11px; text-transform: uppercase;">Material</div>
              <div id="lightboxMaterial" style="color: white; font-size: 14px; font-weight: 500;">-</div>
            </div>
            <div>
              <div style="color: #64748b; font-size: 11px; text-transform: uppercase;">Year Built</div>
              <div id="lightboxYear" style="color: white; font-size: 14px; font-weight: 500;">-</div>
            </div>
            <div>
              <div style="color: #64748b; font-size: 11px; text-transform: uppercase;">ADT</div>
              <div id="lightboxADT" style="color: white; font-size: 14px; font-weight: 500;">-</div>
            </div>
          </div>

          <!-- Defect Notes -->
          <div style="margin-bottom: 24px;">
            <div style="color: #64748b; font-size: 11px; text-transform: uppercase; margin-bottom: 8px;">Condition Notes</div>
            <div id="lightboxNotes" style="color: #cbd5e1; font-size: 13px; line-height: 1.5; background: rgba(255,255,255,0.03); padding: 12px; border-radius: 6px;">-</div>
          </div>

          <!-- Cross-tab Action Buttons -->
          <div style="display: flex; flex-direction: column; gap: 12px; margin-top: auto;">
            <button id="btnLightboxMap" style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); padding: 10px; border-radius: 6px; cursor: pointer; font-weight: 500; transition: 0.2s;">📍 View on Map</button>
            <button id="btnLightboxPDF" style="background: rgba(244, 63, 94, 0.15); color: #f43f5e; border: 1px solid rgba(244, 63, 94, 0.3); padding: 10px; border-radius: 6px; cursor: pointer; font-weight: 500; transition: 0.2s;">📄 Print Inspection Report</button>
          </div>

        </div>
      </div>
    </div>
  </div>
"""

start_idx = html.find('<!-- PHOTOS PANEL -->')
end_idx = html.find('<!-- MAJOR CULVERTS INVENTORY TABLE PANEL -->')

new_html = html[:start_idx] + new_panel + html[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("HTML replaced successfully.")
