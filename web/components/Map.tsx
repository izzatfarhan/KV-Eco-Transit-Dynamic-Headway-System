"use client"

import { MapContainer, TileLayer, Marker, Popup, CircleMarker } from "react-leaflet"
import "leaflet/dist/leaflet.css"
import L from "leaflet"
import { useEffect } from "react"

// Fix for default marker icons in Leaflet with Next.js
const icon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  tooltipAnchor: [16, -28],
  shadowSize: [41, 41]
});

// Mock Data for visualization
const MOCK_STATIONS = [
  { id: 1, name: "KL Sentral", lat: 3.1332, lng: 101.6865, density: 0.8 },
  { id: 2, name: "Pasar Seni", lat: 3.1425, lng: 101.6953, density: 0.4 },
  { id: 3, name: "Masjid Jamek", lat: 3.1495, lng: 101.6965, density: 0.9 },
]

const MOCK_TRAINS = [
  { id: "LRT-KJ-01", lat: 3.1380, lng: 101.6910, status: "Moving", speed: 45 },
  { id: "LRT-KJ-02", lat: 3.1460, lng: 101.6960, status: "Stopped", speed: 0 },
]

export default function Map() {
  return (
    <div className="w-full h-[500px] rounded-xl overflow-hidden border shadow-sm">
      <MapContainer 
        center={[3.1412, 101.6865]} 
        zoom={14} 
        style={{ height: "100%", width: "100%" }}
        zoomControl={false}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
        />

        {/* Render Stations with density indicator */}
        {MOCK_STATIONS.map((station) => (
          <CircleMarker
            key={station.id}
            center={[station.lat, station.lng]}
            radius={station.density > 0.75 ? 12 : 8}
            pathOptions={{
              color: station.density > 0.75 ? "hsl(var(--destructive))" : "hsl(var(--primary))",
              fillColor: station.density > 0.75 ? "hsl(var(--destructive))" : "hsl(var(--primary))",
              fillOpacity: 0.7,
            }}
          >
            <Popup>
              <div className="font-semibold">{station.name}</div>
              <div className="text-sm">Density: {(station.density * 100).toFixed(0)}%</div>
              {station.density > 0.75 && (
                <div className="text-xs text-red-500 font-bold mt-1">Surge Detected!</div>
              )}
            </Popup>
          </CircleMarker>
        ))}

        {/* Render Trains */}
        {MOCK_TRAINS.map((train) => (
          <Marker 
            key={train.id} 
            position={[train.lat, train.lng]}
            icon={icon}
          >
            <Popup>
              <div className="font-semibold">Train {train.id}</div>
              <div className="text-sm">Status: {train.status}</div>
              <div className="text-sm">Speed: {train.speed} km/h</div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  )
}
