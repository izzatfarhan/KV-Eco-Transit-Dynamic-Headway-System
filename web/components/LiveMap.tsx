"use client";

import dynamic from "next/dynamic";
import { Skeleton } from "@/components/ui/skeleton"; // We will create this shadcn component soon

// Dynamically import the Map component to prevent Server-Side Rendering (SSR) issues 
// because Leaflet requires the 'window' object which is unavailable on the server.
const Map = dynamic(() => import("./Map"), { 
  ssr: false,
  loading: () => <Skeleton className="w-full h-[500px] rounded-xl" />
});

export default function LiveMap() {
  return (
    <div className="w-full h-full flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-semibold tracking-tight">Live Telemetry Map</h2>
          <p className="text-sm text-muted-foreground">
            Real-time geospatial visualization of moving block sections and station densities.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="flex h-2 w-2 rounded-full bg-green-500 animate-pulse"></span>
          <span className="text-sm text-muted-foreground font-medium">Live Feed Active</span>
        </div>
      </div>
      <Map />
    </div>
  );
}
