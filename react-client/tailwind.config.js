module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      fontFamily: {
        body: ["Noto Sans KR", "Graphik", "sans-serif"],
      },
      backgroundImage: (theme) => ({
        "profile-img":
          "url('https://i0.wp.com/prikachi.com/wp-content/uploads/2020/07/DPP1.jpg')",
        "detail-profile-img":
          "url('https://images.unsplash.com/photo-1484186139897-d5fc6b908812?ixlib=rb-0.3.5&s=9358d797b2e1370884aa51b0ab94f706&auto=format&fit=crop&w=200&q=80%20500w')",
      }),
    },
  },
  variants: {
    extend: {
      boxShadow: ["focus"],
      ring: ["focus"],
      fontWeight: ["hover"],
      borderWidth: ["hover", "active"],
      borderColor: ["active"],
      scale: ["group-hover"],
      transform: ["group-hover, hover"],
      transitionDuration: ["group-hover, hover"],
      transformOrigin: ["hover", "group-hover"],
      backgroundColor: ["active"],
      transitionDelay: ["hover", "focus"],
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
