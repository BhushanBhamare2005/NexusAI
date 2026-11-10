import { useEffect, useState } from "react";

let pushFn: ((msg: string, tone?: "success" | "error") => void) | null = null;

export function toast(msg: string, tone: "success" | "error" = "success") {
  pushFn?.(msg, tone);
}

export function ToastHost() {
  const [items, setItems] = useState<
    { id: number; msg: string; tone: "success" | "error" }[]
  >([]);

  useEffect(() => {
    pushFn = (msg, tone = "success") => {
      const id = Date.now() + Math.random();
      setItems((p) => [...p, { id, msg, tone }]);
      setTimeout(
        () => setItems((p) => p.filter((x) => x.id !== id)),
        3500
      );
    };
    return () => {
      pushFn = null;
    };
  }, []);

  return (
    <div className="fixed bottom-4 right-4 z-[60] flex flex-col gap-2">
      {items.map((i) => (
        <div
          key={i.id}
          className={`rounded-lg px-4 py-2 text-sm shadow-lg ${
            i.tone === "success"
              ? "bg-nexus-success text-black"
              : "bg-nexus-danger text-white"
          }`}
        >
          {i.msg}
        </div>
      ))}
    </div>
  );
}
