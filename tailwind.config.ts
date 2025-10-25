import type { Config } from "tailwindcss";

export default {
  darkMode: ["class"],
  content: ["./pages/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./app/**/*.{ts,tsx}", "./src/**/*.{ts,tsx}"],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        navy: {
          900: "hsl(var(--navy-900))",
          800: "hsl(var(--navy-800))",
          700: "hsl(var(--navy-700))",
        },
        purple: {
          600: "hsl(var(--purple-600))",
          500: "hsl(var(--purple-500))",
          400: "hsl(var(--purple-400))",
          100: "hsl(var(--purple-100))",
        },
        blue: {
          600: "hsl(var(--blue-600))",
          500: "hsl(var(--blue-500))",
          400: "hsl(var(--blue-400))",
          100: "hsl(var(--blue-100))",
          50: "hsl(var(--blue-50))",
        },
        green: {
          600: "hsl(var(--green-600))",
          500: "hsl(var(--green-500))",
          100: "hsl(var(--green-100))",
          50: "hsl(var(--green-50))",
        },
        gray: {
          900: "hsl(var(--gray-900))",
          700: "hsl(var(--gray-700))",
          600: "hsl(var(--gray-600))",
          500: "hsl(var(--gray-500))",
          400: "hsl(var(--gray-400))",
          300: "hsl(var(--gray-300))",
          200: "hsl(var(--gray-200))",
          100: "hsl(var(--gray-100))",
          50: "hsl(var(--gray-50))",
        },
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        success: {
          DEFAULT: "hsl(var(--success))",
          foreground: "hsl(var(--success-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: {
            height: "0",
          },
          to: {
            height: "var(--radix-accordion-content-height)",
          },
        },
        "accordion-up": {
          from: {
            height: "var(--radix-accordion-content-height)",
          },
          to: {
            height: "0",
          },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config;
