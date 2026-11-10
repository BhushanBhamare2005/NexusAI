import { ButtonHTMLAttributes, forwardRef } from "react";
import clsx from "clsx";

type Variant = "primary" | "ghost" | "danger" | "outline";

interface Props extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
}

const styles: Record<Variant, string> = {
  primary: "bg-nexus-accent text-black hover:bg-nexus-accent/90",
  ghost: "bg-transparent text-slate-200 hover:bg-white/5",
  danger: "bg-nexus-danger text-white hover:bg-nexus-danger/90",
  outline:
    "border border-nexus-border text-slate-200 hover:bg-white/5",
};

export const Button = forwardRef<HTMLButtonElement, Props>(
  ({ className, variant = "primary", ...rest }, ref) => (
    <button
      ref={ref}
      className={clsx(
        "inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2 text-sm font-medium transition disabled:cursor-not-allowed disabled:opacity-50",
        styles[variant],
        className
      )}
      {...rest}
    />
  )
);
Button.displayName = "Button";
