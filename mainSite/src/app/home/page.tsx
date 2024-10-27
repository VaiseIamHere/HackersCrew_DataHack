"use client";
import React from 'react';
import { SidebarDemo } from '../components/Sidebar_home';
import Footer from '../components/Footer';

const Home = () => {
  return (
    <div className="flex flex-col min-h-screen"> {/* Flexbox layout to occupy full height */}
      <div className="flex-grow"> {/* This will take up the available space */}
        <SidebarDemo />
      </div>
      <Footer />
    </div>
  );
};

export default Home;
