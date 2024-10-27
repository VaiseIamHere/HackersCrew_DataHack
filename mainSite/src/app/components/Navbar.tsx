"use client";

import React, { useState } from "react";
import { HoveredLink, Menu, MenuItem } from "./ui/navbar-menu";
import { cn } from "../../utils/cn"
import Link from "next/link";

export function NavbarDemo() {
  return (
    <div className="relative w-full flex items-center justify-center">
      <Navbar className="top-2" />
    </div>
  );
}

function Navbar({ className }: { className?: string }) {
  const [active, setActive] = useState<string | null>(null);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <div
      className={cn(
        "fixed top-4 inset-x-0 max-w-2xl mx-auto z-50",
        className
      )}
    >
      <div className="flex items-center justify-between p-4 bg-white shadow-md rounded-lg">
        <Link href="/home">
          <span className="text-xl font-bold">Brainwave</span>
        </Link>
        
        {/* Hamburger menu for small screens */}
        <button
          className="md:hidden"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 6h16M4 12h16m-7 6h7"
            />
          </svg>
        </button>

        {/* Menu for larger screens */}
        <div className="hidden md:block">
          <Menu setActive={setActive}>
            <MenuItem setActive={setActive} active={active} item="Account">
              <div className="flex flex-col space-y-4 text-sm">
                <HoveredLink href="/signin">Login</HoveredLink>
                <HoveredLink href="/account">View Profile</HoveredLink>
              </div>
            </MenuItem>
            <Link href="/home"><MenuItem setActive={setActive} active={active} item="Home" /></Link>
          </Menu>
        </div>
      </div>

      {/* Mobile menu */}
      {isMenuOpen && (
        <div className="md:hidden mt-2 bg-white shadow-md rounded-lg">
          <Link href="/home"><div className="p-4 hover:bg-gray-100">Home</div></Link>
          <Link href="/premium"><div className="p-4 hover:bg-gray-100">Premium</div></Link>
          <Link href="/library"><div className="p-4 hover:bg-gray-100">Library</div></Link>
          <Link href="/search"><div className="p-4 hover:bg-gray-100">Search</div></Link>
          <div className="p-4 hover:bg-gray-100">
            <details>
              <summary>Account</summary>
              <div className="ml-4 mt-2 flex flex-col space-y-2">
                <Link href="/web-dev">Login</Link>
                <Link href="/interface-design">View Profile</Link>
                <Link href="/seo">Listening history</Link>
                <Link href="/branding">Settings and privacy</Link>
              </div>
            </details>
          </div>
        </div>
      )}
    </div>
  );
}