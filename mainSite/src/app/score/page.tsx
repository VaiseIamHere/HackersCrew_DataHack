"use client";
import React from 'react';
import { SidebarScore } from '../components/Sidebar_Score';
import Footer from '../components/Footer';

const Page = () => {
  return (
    <div className="flex flex-col h-screen bg-white">
      <div className="flex flex-1">
        <SidebarScore />
      </div>
      <Footer />
    </div>
  );
}

export default Page;
