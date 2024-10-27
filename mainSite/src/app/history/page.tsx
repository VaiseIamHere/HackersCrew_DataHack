"use client"
import React from 'react'
import { SidebarHistory } from '../components/Sidebar_History'
import Footer from '../components/Footer'

const page = () => {
  return (<>
    <div>
        <SidebarHistory />
    </div>
    <Footer />
    </>
  )
}

export default page