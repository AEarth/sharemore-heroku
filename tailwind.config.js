/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./core/templates/**/*.html"],
  daisyui:{
    themes: [
      {
        mytheme: {
    "primary": "#5645a1",
    "secondary": "#dfd6c8",  
    "accent": "#00d1ff",     
    "neutral": "#29261b",     
    "base-100": "#3d3929",     
    "info": "#dfd6c8",     
    "success": "#00f05f",     
    "warning": "#ffbc55",    
    "error": "#ff7295",
            },
      },
    ],
},

plugins: [require("daisyui")],
};
