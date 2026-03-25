// StatsPanel.tsx
import { Tabs } from "@/components/ui/tabs";

interface StatsPanelProps {
  defaultValue: string;
  label?: string;
  children: React.ReactNode;
}

export function StatsPanel({ defaultValue, label, children }: StatsPanelProps) {
  return (
    <div className="flex flex-col h-[600px] rounded-lg border border-border bg-card">
      {label && (
        <div className="px-4 pt-4 pb-2 text-sm font-semibold text-muted-foreground uppercase tracking-wider shrink-0">
          {label}
        </div>
      )}
      <Tabs
        defaultValue={defaultValue}
        className="flex flex-col flex-1 min-h-0 px-4 pb-4"
      >
        {children}
      </Tabs>
    </div>
  );
}
