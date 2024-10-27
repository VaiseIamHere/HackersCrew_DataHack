import React from 'react';
import { SidebarUpload } from '../components/Sidebar_Upload';
import Footer from '../components/Footer';

const Page = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <div className="flex-grow">
        <SidebarUpload />
      </div>
      <Footer />
    </div>
  );
};

export default Page;
