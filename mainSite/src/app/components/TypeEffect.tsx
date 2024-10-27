"use client";
import { TypewriterEffectSmooth } from "./ui/typewriter-effect";
export function TypewriterEffectSmoothDemo() {
  const words = [
    {
      text: "Evaluate",
    },
    {
      text: "Your ",
    },
    {
      text: "Learning Experience at",
    },
    
    {
      text: "BrainWave.",
      className: "text-blue-500 dark:text-blue-500",
    },
  ];
  return (
    <div className="flex flex-col items-center justify-center h-[60rem]  ">
      <TypewriterEffectSmooth words={words} />
    </div>
  );
}
