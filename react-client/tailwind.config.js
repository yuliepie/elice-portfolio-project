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
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
