import LiveMap from "@/components/LiveMap"
import ChatInterface from "@/components/ChatInterface"
import { Train } from "lucide-react"

export default function Home() {
  return (
    <main className="min-h-screen bg-background flex flex-col p-6 max-w-7xl mx-auto gap-6">
      <header className="flex items-center gap-3 pb-4 border-b">
        <div className="bg-primary p-2 rounded-lg text-primary-foreground">
          <Train className="h-6 w-6" />
        </div>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Klang Valley Eco-Transit Optimizer</h1>
          <p className="text-muted-foreground">Operator Control Dashboard</p>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1">
        <section className="lg:col-span-2 flex flex-col gap-4 bg-card rounded-xl border p-6 shadow-sm">
          <LiveMap />
        </section>
        
        <section className="flex flex-col gap-4">
          <ChatInterface />
          
          <div className="bg-card rounded-xl border p-6 shadow-sm flex-1">
            <h3 className="font-semibold mb-2">System Status</h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center text-sm">
                <span className="text-muted-foreground">Network Load</span>
                <span className="font-medium text-amber-500">Moderate (65%)</span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-muted-foreground">Active Trains</span>
                <span className="font-medium">42 / 50</span>
              </div>
              <div className="flex justify-between items-center text-sm">
                <span className="text-muted-foreground">Avg Headway</span>
                <span className="font-medium">180s</span>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  )
}
