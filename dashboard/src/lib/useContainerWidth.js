import { useEffect, useRef, useState } from "react";

// Measure the width of a container, so a chart can fill it and resize with the page.
// Usage: const [ref, width] = useContainerWidth(); <div ref={ref}>{width > 0 && <Chart width={width} />}</div>
export function useContainerWidth() {
  const ref = useRef(null);
  const [width, setWidth] = useState(0);

  useEffect(() => {
    if (!ref.current) return undefined;
    const observer = new ResizeObserver(([entry]) => setWidth(entry.contentRect.width));
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return [ref, width];
}
