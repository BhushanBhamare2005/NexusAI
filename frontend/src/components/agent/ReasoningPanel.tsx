import { useState } from "react";
import { ChevronDown, ChevronRight } from "lucide-react";

interface Props {
  title?: string;
  children: React.ReactNode;
}

export default function ReasoningPanel({ title = "Reasoning", children }: Props) {
  const [open, setOpen] = useState(true);
  return (
    <div className="rounded-lg border border-nexus-border/60 bg-nexus-bg/40">
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex w-full items-center gap-2 px-3 py-2 text-xs text-nexus-muted hover:text-white"
      >
        {open ? <ChevronDown size={12} /> : <ChevronRight size={12} />}
        {title}
      </button>
      {open && (
        <div className="border-t border-nexus-border/60 px-3 py-2 text-xs text-slate-300">
          {children}
        </div>
      )}
    </div>
  );
}
