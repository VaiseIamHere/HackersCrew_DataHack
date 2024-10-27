"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";

let interval: any;

type Card = {
  id: number;
  name: string;
  designation: string;
  content: React.ReactNode;
};

export const CardStack = ({
  items,
  activeIndex,
  offset,
  scaleFactor,
}: {
  items: Card[];
  activeIndex: number;
  offset?: number;
  scaleFactor?: number;
}) => {
  const CARD_OFFSET = offset || 20; // Increased offset for spacing
  const SCALE_FACTOR = scaleFactor || 0.06;

  return (
    <div className="relative h-80 w-80 md:h-96 md:w-96"> {/* Increased size */}
      {items.map((card, index) => {
        if (index !== activeIndex) return null; // Render only the active card

        return (
          <motion.div
            key={card.id}
            className="absolute dark:bg-black bg-white h-80 w-80 md:h-96 md:w-96 rounded-3xl p-4 shadow-xl border border-neutral-200 dark:border-white/[0.1] shadow-black/[0.1] dark:shadow-white/[0.05] flex flex-col justify-between"
            style={{
              transformOrigin: "top center",
            }}
            animate={{
              top: 0,
              scale: 1,
              zIndex: items.length,
            }}
          >
            <div className="font-normal text-neutral-700 dark:text-neutral-200">
              {card.content}
            </div>
            <div>
              <p className="text-neutral-500 font-medium dark:text-white">
                {card.name}
              </p>
              <p className="text-neutral-400 font-normal dark:text-neutral-200">
                {card.designation}
              </p>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
};
