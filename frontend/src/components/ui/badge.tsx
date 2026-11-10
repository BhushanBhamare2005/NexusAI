import { HTMLAttributes } from "react";
import clsx from "clsx";

type Tone = "neutral" | "success" | "warn" | "danger" | "accent";

const tones: Record<Tone, string> = {
  neutral: "bg-white/5 text-slate-300",
  success: "bg-nexus-success/15 text-nexus-success",
  warn: "bg-nexus-warn/15 text-nexus-warn",
  danger: "bg-nexus-danger/15 text-nexus-danger",
  accent: "bg-nexus-accent/15 text-nexus-accent",
};

interface Props extends HTMLAttributes<HTMLSpanElement> {
  tone?: Tone;
}

export function Badge({ tone = "neutral", className, ...rest }: Props) {
  return (
    <span
      className={clsx(
        "inline-flex items-center rounded-full px-2 py-0.5 text-[11px] font-medium",
        tones[tone],
        className
      )}
      {...rest}
    />
  );
}
