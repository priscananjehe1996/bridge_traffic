import sys

js = """
// ==========================================
// PHOTO ALBUM LOGIC
// ==========================================

let galleryStructures = [];
let currentGalleryFilter = { search: '', type: 'all', condition: 'all' };
let currentLightboxIndex = 0;
let currentLightboxPhotos = [];
let currentLightboxPhotoIndex = 0;
let filteredGallery = [];

function initPhotoGallery() {
    galleryStructures = [];
    
    // Process Bridges
    if (typeof BRIDGES !== 'undefined') {
        BRIDGES.forEach(b => {
            const id = String(b.bridge_no || b._id || '').trim();
            const photos = PHOTOS_DATA[id] || [];
            galleryStructures.push({
                type: 'bridge',
                id: id,
                name: b.bridge_nam || 'Unknown Bridge',
                district: b.district || b.region || 'Unknown',
                road: b.link_name || b.road_no || 'Unknown Road',
                conditionNum: b.overall_rating || b.condition_rating || b.overall_cond || null,
                conditionCat: b.condition_category || 'Unknown',
                span: b.bridge_len || b.span_diameter || '-',
                material: bmsCodeDescription('type_material', b.type_material) || '-',
                year: b.year_built || '-',
                adt: b.aadt_rebuilt_2026 || b.aadt_2025 || '-',
                notes: b.overall_rating_notes || b.general_notes || '-',
                photos: photos,
                chainage: b.km || b.chainage_validated_km || '-',
                lat: b.map_y || b.y_new,
                lon: b.map_x || b.x_new,
                link_id: b.link_no
            });
        });
    }

    // Process Culverts
    if (typeof MAJOR_CULVERTS !== 'undefined') {
        MAJOR_CULVERTS.forEach(c => {
            const id = String(c.culvert_no || c.bridge_no || c._id || '').trim();
            const photos = PHOTOS_DATA[id] || [];
            galleryStructures.push({
                type: 'culvert',
                id: id,
                name: c.bridge_nam || c.culvert_nam || 'Major Culvert',
                district: c.district || c.region || 'Unknown',
                road: c.link_name || c.road || 'Unknown Road',
                conditionNum: c.overall_cond || c.overall_rating || c.condition_rating || null,
                conditionCat: c.condition_category || 'Unknown',
                span: c.span_diameter || c.diameter || '-',
                material: c.type_material ? bmsCodeDescription('type_material', c.type_material) : '-',
                year: c.year_built || '-',
                adt: c.aadt_rebuilt_2026 || c.aadt_2025 || '-',
                notes: c.overall_cond_notes || c.general_notes || '-',
                photos: photos,
                chainage: c.km || c.chainage_validated_km || '-',
                lat: c.map_y || c.y_new,
                lon: c.map_x || c.x_new,
                link_id: c.link_no
            });
        });
    }

    // Bind UI
    document.getElementById('photoGallerySearch')?.addEventListener('input', e => {
        currentGalleryFilter.search = e.target.value.toLowerCase();
        renderPhotoGallery();
    });
    document.getElementById('photoFilterType')?.addEventListener('change', e => {
        currentGalleryFilter.type = e.target.value;
        renderPhotoGallery();
    });
    document.getElementById('photoFilterCondition')?.addEventListener('change', e => {
        currentGalleryFilter.condition = e.target.value;
        renderPhotoGallery();
    });

    document.getElementById('lightboxClose')?.addEventListener('click', closeLightbox);
    document.getElementById('lightboxPrev')?.addEventListener('click', () => changeLightboxPhoto(-1));
    document.getElementById('lightboxNext')?.addEventListener('click', () => changeLightboxPhoto(1));

    document.getElementById('btnLightboxMap')?.addEventListener('click', () => {
        closeLightbox();
        const tab = document.querySelector('[data-tab="spatial-map"]');
        if(tab) tab.click();
        const s = filteredGallery[currentLightboxIndex];
        if (s && s.lon && s.lat) {
            mapOffsetX = canvas.width / 2 - getProjection(s.lon, s.lat, canvas.width, canvas.height).x;
            mapOffsetY = canvas.height / 2 - getProjection(s.lon, s.lat, canvas.width, canvas.height).y;
            drawMap();
        }
    });

    renderPhotoGallery();
}

function getConditionColorClass(cat) {
    if (!cat) return 'unknown';
    const c = cat.toLowerCase();
    if (c.includes('good') || c.includes('excellent')) return 'good';
    if (c.includes('fair')) return 'fair';
    if (c.includes('poor') || c.includes('critical') || c.includes('bad')) return 'critical';
    return 'unknown';
}

function renderPhotoGallery() {
    filteredGallery = galleryStructures.filter(s => {
        if (currentGalleryFilter.type !== 'all' && s.type !== currentGalleryFilter.type) return false;
        if (currentGalleryFilter.condition !== 'all') {
            const cClass = getConditionColorClass(s.conditionCat);
            if (cClass !== currentGalleryFilter.condition) return false;
        }
        if (currentGalleryFilter.search) {
            const q = currentGalleryFilter.search;
            return (s.id.toLowerCase().includes(q) || s.road.toLowerCase().includes(q) || s.district.toLowerCase().includes(q));
        }
        return true;
    });

    // Update Heatmap
    const heatmap = document.getElementById('photoHeatmap');
    if (heatmap) {
        const counts = { good: 0, fair: 0, critical: 0, unknown: 0 };
        filteredGallery.forEach(s => counts[getConditionColorClass(s.conditionCat)]++);
        const total = filteredGallery.length || 1;
        heatmap.innerHTML = `
            <div style="width: ${counts.good/total*100}%; background: #10b981;"></div>
            <div style="width: ${counts.fair/total*100}%; background: #f59e0b;"></div>
            <div style="width: ${counts.critical/total*100}%; background: #ef4444;"></div>
            <div style="width: ${counts.unknown/total*100}%; background: #64748b;"></div>
        `;
    }

    const grid = document.getElementById('photoMainGrid');
    if (!grid) return;

    if (filteredGallery.length === 0) {
        grid.innerHTML = '<div class="empty-state"><p>No structures match your filters.</p></div>';
        return;
    }

    // Lazy rendering for performance - slice first 100
    const displayList = filteredGallery.slice(0, 200);

    grid.innerHTML = displayList.map((s, idx) => {
        const cClass = getConditionColorClass(s.conditionCat);
        const thumb = s.photos.length > 0 ? s.photos[0] : 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300" fill="%231e293b"><rect width="100%" height="100%"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="24" fill="%23475569">No Photo Available</text></svg>';
        
        return `
            <div class="photo-card" data-condition="${cClass}" onclick="openLightbox(${idx})">
                <div class="photo-card-img-container">
                    <img src="${thumb}" loading="lazy" alt="Structure ${s.id}">
                </div>
                <div class="photo-card-body">
                    <div class="photo-card-title">
                        ${s.id}
                        <div class="condition-ring ring-${cClass}" title="${s.conditionCat}"></div>
                    </div>
                    <div class="photo-card-subtitle">${s.road} &bull; ${s.district}</div>
                    
                    <div class="photo-card-hover-details">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                            <span>Span: ${s.span}m</span>
                            <span>Built: ${s.year}</span>
                        </div>
                        <div>Material: ${s.material}</div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function openLightbox(index) {
    if (!filteredGallery[index]) return;
    currentLightboxIndex = index;
    const s = filteredGallery[index];
    currentLightboxPhotos = s.photos.length > 0 ? s.photos : ['data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" fill="%230f172a"><rect width="100%" height="100%"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="32" fill="%23475569">No Photo Available</text></svg>'];
    currentLightboxPhotoIndex = 0;
    
    // Update metadata
    document.getElementById('lightboxTitle').innerText = s.id + (s.name !== 'Unknown Bridge' && s.name !== 'Major Culvert' ? ' - ' + s.name : '');
    document.getElementById('lightboxSubtitle').innerText = `${s.road} • ${s.district} • CH ${s.chainage} km`;
    document.getElementById('lightboxSpan').innerText = s.span ? s.span + ' m' : '-';
    document.getElementById('lightboxMaterial').innerText = s.material || '-';
    document.getElementById('lightboxYear').innerText = s.year || '-';
    document.getElementById('lightboxADT').innerText = s.adt || '-';
    document.getElementById('lightboxNotes').innerText = s.notes || '-';
    
    const cClass = getConditionColorClass(s.conditionCat);
    const ring = document.getElementById('lightboxConditionRing');
    ring.className = '';
    ring.style.borderColor = cClass === 'good' ? '#10b981' : cClass === 'fair' ? '#f59e0b' : cClass === 'critical' ? '#ef4444' : '#64748b';
    ring.innerText = s.conditionNum || '-';

    updateLightboxImage();
    
    document.getElementById('photoLightbox').style.display = 'flex';
}

function closeLightbox() {
    document.getElementById('photoLightbox').style.display = 'none';
}

function changeLightboxPhoto(dir) {
    currentLightboxPhotoIndex += dir;
    if (currentLightboxPhotoIndex < 0) currentLightboxPhotoIndex = currentLightboxPhotos.length - 1;
    if (currentLightboxPhotoIndex >= currentLightboxPhotos.length) currentLightboxPhotoIndex = 0;
    updateLightboxImage();
}

function updateLightboxImage() {
    document.getElementById('lightboxImage').src = currentLightboxPhotos[currentLightboxPhotoIndex];
    
    const filmstrip = document.getElementById('lightboxFilmstrip');
    if (currentLightboxPhotos.length > 1) {
        filmstrip.style.display = 'flex';
        filmstrip.innerHTML = currentLightboxPhotos.map((p, i) => `
            <img src="${p}" class="filmstrip-thumb ${i === currentLightboxPhotoIndex ? 'active' : ''}" onclick="currentLightboxPhotoIndex = ${i}; updateLightboxImage();">
        `).join('');
    } else {
        filmstrip.style.display = 'none';
    }
}

// Hook into the initialization
const oldAppJsInit = window.onload;
window.onload = function() {
    if (oldAppJsInit) oldAppJsInit();
    setTimeout(initPhotoGallery, 1500); // Wait for data to load
};

"""

with open('app.js', 'a', encoding='utf-8') as f:
    f.write(js)

print("JS added successfully.")
