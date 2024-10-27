"use client";
import { useState } from "react";
import { CardStack } from "./ui/card-stack";
import { cn } from "@/lib/utils";
import { ArrowRight, Check, X } from "lucide-react"; // Importing icons

export function CardStackDemo() {
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [score, setScore] = useState<number>(0);
  const [currentCardIndex, setCurrentCardIndex] = useState<number>(0);

  const handleOptionSelect = (option: string) => {
    setSelectedOption(option);
  };

  const handleSubmit = () => {
    if (selectedOption === CARDS[currentCardIndex].correctAnswer) {
      setScore((prevScore) => prevScore + 1);
    }
    setSelectedOption(null); // Reset the selected option after submitting
    handleNext(); // Automatically go to the next card after submitting
  };

  const handleNext = () => {
    setCurrentCardIndex((prevIndex) => (prevIndex + 1) % CARDS.length);
    setSelectedOption(null); // Reset the selected option for the next card
  };

  const handleSkip = () => {
    handleNext(); // Skip to the next card
  };

  return (
    <div className="h-[40rem] flex flex-col items-center justify-center w-full">
      <CardStack items={CARDS} activeIndex={currentCardIndex} />
      <div className="mt-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {CARDS[currentCardIndex].options.map((option) => (
            <button
              key={option}
              className={cn(
                "border p-4 rounded-lg transition-all",
                selectedOption === option ? "bg-blue-500 text-white" : "bg-white"
              )}
              onClick={() => handleOptionSelect(option)}
            >
              {option}
            </button>
          ))}
        </div>
        <div className="flex gap-4 mt-6"> {/* Increased margin from mt-4 to mt-6 */}
          <button
            onClick={handleSubmit}
            className="flex items-center justify-center px-6 py-3 bg-green-600 text-white rounded-lg shadow-md transition-transform transform hover:scale-105 active:scale-95"
            disabled={!selectedOption}
          >
            <Check className="w-5 h-5 mr-2" /> {/* Check icon for submit */}
            Submit
          </button>
          <button
            onClick={handleNext}
            className="flex items-center justify-center px-6 py-3 bg-blue-600 text-white rounded-lg shadow-md transition-transform transform hover:scale-105 active:scale-95"
          >
            <ArrowRight className="w-5 h-5 mr-2" /> {/* Arrow icon for next */}
            Next
          </button>
          <button
            onClick={handleSkip}
            className="flex items-center justify-center px-6 py-3 bg-red-600 text-white rounded-lg shadow-md transition-transform transform hover:scale-105 active:scale-95"
          >
            <X className="w-5 h-5 mr-2" /> {/* X icon for skip */}
            Skip
          </button>
        </div>
        <div className="mt-4">Score: {score}</div>
      </div>
    </div>
  );
}

// Highlight component
export const Highlight = ({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) => {
  return (
    <span
      className={cn(
        "font-bold bg-emerald-100 text-emerald-700 dark:bg-emerald-700/[0.2] dark:text-emerald-500 px-1 py-0.5",
        className
      )}
    >
      {children}
    </span>
  );
};

const CARDS = [
  {
    id: 0,
    name: "Difficulty:7",
    designation: "Computer Science",
    content: (
      <p>
        Which data structure is used to implement recursion?
      </p>
    ),
    options: ["Queue", "Stack", "Array", "Linked List"],
    correctAnswer: "Stack",
  },
  {
    id: 1,
    name: "Difficulty:5",
    designation: "Computer Science",
    content: (
      <p>
        Given an array of integers, find the maximum sum of a contiguous subarray.
      </p>
    ),
    options: ["Kadane's Algorithm", "Divide and Conquer", "Dynamic Programming", "Greedy Algorithm"],
    correctAnswer: "Kadane's Algorithm",
  },
  {
    id: 2,
    name: "Difficulty:6",
    designation: "Computer Science",
    content: (
      <p>
        What is the time complexity of accessing an element in an array?
      </p>
    ),
    options: ["O(n)", "O(log n)", "O(1)", "O(n log n)"],
    correctAnswer: "O(1)",
  },
];
