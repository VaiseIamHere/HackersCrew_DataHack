"use client";
import React from 'react';
import { Music, Heart, Share2 } from 'lucide-react';

interface FloatingBubbleProps {
  left: string;
  top: string;
  size: number;
  duration: number;
}

const FloatingBubble: React.FC<FloatingBubbleProps> = ({ left, top, size, duration }) => (
  <div
    className="absolute rounded-full bg-gradient-to-r from-purple-500 to-pink-500"
    style={{
      left,
      top,
      width: `${size}px`,
      height: `${size}px`,
      animation: `float ${duration}s infinite ease-in-out`
    }}
  />
);

const Footer: React.FC = () => {
  const bubbles: FloatingBubbleProps[] = Array.from({ length: 20 }, () => ({
    left: `${Math.random() * 100}%`,
    top: `${Math.random() * 100}%`,
    size: Math.random() * 50 + 10,
    duration: Math.random() * 10 + 5
  }));

  return (
    <footer className="bg-black text-white p-6 relative overflow-hidden">
      <div className="container mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <h3 className="text-2xl font-bold mb-2">BrainWave</h3>
            <p className="text-sm opacity-70">Your learning, your way</p>
          </div>
          <div className="flex space-x-4">
            <a href="#" className="hover:text-purple-400 transition-colors duration-300">
              <Music size={24} />
            </a>
            <a href="#" className="hover:text-red-400 transition-colors duration-300">
              <Heart size={24} />
            </a>
            <a href="#" className="hover:text-blue-400 transition-colors duration-300">
              <Share2 size={24} />
            </a>
          </div>
        </div>
        <div className="mt-6 text-center text-sm opacity-50">
          © 2024 BrainWave. All rights reserved.
          @Hackers Crew
        </div>
      </div>
      <div className="absolute inset-0 opacity-10 overflow-hidden pointer-events-none">
        {bubbles.map((props, index) => (
          <FloatingBubble key={index} {...props} />
        ))}
      </div>
      <style jsx>{`
        @keyframes float {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-20px); }
        }
      `}</style>
    </footer>
  );
};

export default Footer;