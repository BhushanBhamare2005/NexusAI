import {
  HTMLAttributes,
  ReactNode,
  TdHTMLAttributes,
  ThHTMLAttributes,
} from "react";
import clsx from "clsx";

export function Table({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <div className={clsx("overflow-x-auto", className)}>
      <table className="min-w-full text-left text-sm">{children}</table>
    </div>
  );
}

export function THead(props: HTMLAttributes<HTMLTableSectionElement>) {
  return (
    <thead
      className="border-b border-nexus-border text-xs uppercase tracking-wide text-nexus-muted"
      {...props}
    />
  );
}

export function TR(props: HTMLAttributes<HTMLTableRowElement>) {
  return <tr className="border-b border-nexus-border/60" {...props} />;
}

export function TH(props: ThHTMLAttributes<HTMLTableCellElement>) {
  return <th className="px-3 py-2 font-medium" {...props} />;
}

export function TD(props: TdHTMLAttributes<HTMLTableCellElement>) {
  return <td className="px-3 py-2 text-slate-200" {...props} />;
}
