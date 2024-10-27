"use client";
import { AnimatedPinDemo } from "./components/Card";
import { HeroScrollDemo } from "./components/Container_Scroll";
import Footer from "./components/Footer";
import { HeroParallaxDemo } from "./components/Homecover";
import { NavbarDemo } from "./components/Navbar";
import { TypewriterEffectSmoothDemo } from "./components/TypeEffect";

export default function Home() {
  return (
    <div >
     <NavbarDemo />
     <HeroScrollDemo />
     <HeroParallaxDemo />
     <TypewriterEffectSmoothDemo />
     <AnimatedPinDemo />
     <Footer />
    </div>
  );
}
