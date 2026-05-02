---
name: Civic Clarity
colors:
  surface: '#f7f9ff'
  surface-dim: '#d7dadf'
  surface-bright: '#f7f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f4f9'
  surface-container: '#ebeef3'
  surface-container-high: '#e5e8ee'
  surface-container-highest: '#e0e3e8'
  on-surface: '#181c20'
  on-surface-variant: '#43474f'
  inverse-surface: '#2d3135'
  inverse-on-surface: '#eef1f6'
  outline: '#737780'
  outline-variant: '#c3c6d1'
  surface-tint: '#3a5f94'
  primary: '#001e40'
  on-primary: '#ffffff'
  primary-container: '#003366'
  on-primary-container: '#799dd6'
  inverse-primary: '#a7c8ff'
  secondary: '#005cba'
  on-secondary: '#ffffff'
  secondary-container: '#5095fe'
  on-secondary-container: '#002d61'
  tertiary: '#181f25'
  on-tertiary: '#ffffff'
  tertiary-container: '#2d343a'
  on-tertiary-container: '#959ca4'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d5e3ff'
  primary-fixed-dim: '#a7c8ff'
  on-primary-fixed: '#001b3c'
  on-primary-fixed-variant: '#1f477b'
  secondary-fixed: '#d7e3ff'
  secondary-fixed-dim: '#aac7ff'
  on-secondary-fixed: '#001b3e'
  on-secondary-fixed-variant: '#00458e'
  tertiary-fixed: '#dce3eb'
  tertiary-fixed-dim: '#c0c7cf'
  on-tertiary-fixed: '#151c22'
  on-tertiary-fixed-variant: '#40484e'
  background: '#f7f9ff'
  on-background: '#181c20'
  surface-variant: '#e0e3e8'
typography:
  headline-lg:
    fontFamily: Public Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Public Sans
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Public Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Public Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Public Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Public Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Public Sans
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-padding: 24px
  gutter: 16px
  stack-sm: 12px
  stack-md: 24px
  stack-lg: 48px
---

## Brand & Style

The design system is anchored in the principles of transparency, accessibility, and institutional reliability. The brand personality is that of a "Trusted Guide"—authoritative enough to provide official election data, yet approachable enough to encourage civic participation from all demographics.

The aesthetic follows a **Corporate / Modern** style with strong **Minimalist** influences. By prioritizing clarity over decoration, the design system ensures that complex information regarding ballots, polling locations, and deadlines remains the focal point. The visual language uses generous whitespace to reduce cognitive load, ensuring the user feels calm and informed rather than overwhelmed by the political process.

## Colors

The color palette is designed to evoke a sense of national stability and digital modernization.

*   **Primary (Navy Blue):** Used for headers, primary branding, and structural elements to establish authority and trust.
*   **Secondary (Action Blue):** A brighter blue reserved for interactive elements, ensuring high visibility for buttons and links.
*   **Tertiary (Soft Sky):** Used for subtle backgrounds and container fills to differentiate content sections without adding visual noise.
*   **Neutrals:** A range of subtle grays (from `#F8F9FA` to `#495057`) manages secondary text and borders, while a near-black is used for body text to maintain WCAG AAA contrast ratios.

The system defaults to a **Light Mode** to mimic the familiarity of official documents and paper ballots, emphasizing cleanliness and legibility.

## Typography

The design system utilizes **Public Sans**, an open-source typeface designed for government interfaces. It provides a clean, neutral, and highly legible sans-serif experience that performs exceptionally well across various screen sizes.

Typographic hierarchy is strictly enforced to guide users through the information architecture. Headlines use a heavier weight and tighter letter spacing to command attention, while body text uses a generous 1.5x line height to ensure readability for long-form descriptions of ballot measures. For maximum accessibility, the base body size is set to a highly legible 16px, scaling up to 18px for key informational blocks.

## Layout & Spacing

The design system employs a **Fixed Grid** model for desktop environments (12 columns, 1200px max-width) and a **Fluid Grid** for mobile devices to ensure the experience remains consistent on the go.

The spacing rhythm is built on an 8px base unit.
*   **Vertical Rhythm:** Generous stack spacing (24px to 48px) is used between content sections to prevent the UI from feeling "cluttered" or "political."
*   **Safe Areas:** Large 24px margins are maintained on mobile devices to ensure interactive elements are not too close to the screen edges, aiding users with limited motor dexterity.

## Elevation & Depth

Visual hierarchy is primarily achieved through **Tonal Layers** rather than heavy shadows. This keeps the interface feeling "flat" and "official," similar to modern civic websites.

*   **Surface Tiers:** The main background is white, while secondary content containers use a subtle gray or soft blue fill.
*   **Elevation Shadows:** Only used for floating action buttons or active modal dialogs. These shadows are "Ambient"—extremely diffused with low opacity (10%) and a slight navy tint to maintain color harmony.
*   **Interactive State:** Elements like cards or buttons do not "lift" on hover; instead, they use subtle border weight changes or color shifts to indicate interactivity, maintaining a grounded and stable feel.

## Shapes

The design system utilizes a **Rounded** shape language (Level 2). This choice balances the seriousness of the content with an approachable, modern feel.

*   **Standard Elements:** Buttons and input fields use a 0.5rem (8px) corner radius.
*   **Large Containers:** Cards and informational modules use a 1rem (16px) radius to soften the layout.
*   **Interactive Icons:** Circular containers (pill-shaped) are used for progress indicators and status badges (e.g., "Registered" or "Voted") to distinguish them from structural content.

## Components

The components within the design system prioritize touch-targets and clarity:

*   **Buttons:** Primary actions use a large format (min-height: 56px) with high-contrast white text on the Primary Navy background. Secondary buttons use an outlined style with a 2px stroke to ensure they are visible but subordinate.
*   **Cards:** Used to group election dates or candidate profiles. They feature a 1px soft gray border and 24px internal padding to provide a "breathable" content area.
*   **Input Fields:** Labels are always persistent (not floating) to maximize accessibility. Fields include a clear focus state with a 3px "Action Blue" ring.
*   **Progress Indicators:** A horizontal "Step Tracker" is essential for long processes like registration, using the secondary blue to show completed steps and a light gray for pending ones.
*   **Chips:** Used for filtering "Local," "State," or "Federal" contests. These utilize the pill-shape for easy differentiation from buttons.
*   **Status Banners:** High-priority alerts (e.g., "Election Tomorrow") use a subtle blue background with a left-accent border in the secondary color to draw the eye without creating a sense of "alarm" or "danger."
