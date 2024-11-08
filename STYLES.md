# Agri E-commerce Style Guide

## Color Palette

### Primary Colors
- Forest Green: `#28a745` (Primary buttons, CTAs)
- Dark Green: `#218838` (Button hover states)
- Warm Beige: `#FAF7F2` (Background)
- Dark Beige: `#E5E0D8` (Secondary elements)
- White: `#ffffff` (Card backgrounds)

### Text Colors
- Primary Text: `#2D2D2D` (Headings)
- Secondary Text: `#4A4A4A` (Subtitles)
- Gray Text: `#555555` (Body text)
- Light Text: `#f0f0f0` (Text on dark backgrounds)
- Footer Text: `#cccccc`

### UI States
- Primary Button: `#28a745`
- Button Hover: `#218838`
- Border Color: `#e0e0e0`
- Shadow Color: `rgba(0, 0, 0, 0.1)`

## Typography

### Font Families
- Primary: 'Poppins', sans-serif
- Secondary: 'Arial', sans-serif
- Headings: 'Montserrat', sans-serif

### Font Sizes
- Hero Title: 2.5rem
- Section Headers: 2rem
- Card Titles: 1.5rem
- Navigation: 1.2rem
- Body Text: 1rem
- Small Text: 0.875rem
- Footer Text: 0.9em

### Font Weights
- Regular: 400
- Medium: 500
- Bold: 700

## Layout

### Spacing
- Container Padding: 20px
- Section Padding: 40px 20px
- Card Padding: 15px
- Button Padding: 8px 12px (small), 15px 30px (large)
- Grid Gap: 20px

### Breakpoints
- Mobile: 480px
- Tablet: 768px
- Laptop: 1024px
- Desktop: 1200px

## Components

### Buttons
css
.btn {
padding: 0.875rem 1.5rem;
border-radius: 10px;
font-weight: 500;
transition: all 0.2s ease;
}
.btn-primary {
background: #28a745;
color: white;
}
.btn-primary:hover {
background: #218838;
}

### Cards
```css
.card {
    background: #ffffff;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}
```

### Form Elements
```css
.form-group input,
.form-group select,
.form-group textarea {
    padding: 0.875rem 1rem;
    border: 1.5px solid #E2E8F0;
    border-radius: 10px;
    transition: all 0.2s ease;
}

.form-group input:focus {
    border-color: #28a745;
    box-shadow: 0 0 0 3px rgba(40, 167, 69, 0.1);
}
```

### Grid System
```css
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
}
```

### Container
```css
.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
}
```

## Animations

### Transitions
```css
/* Standard transition */
transition: all 0.2s ease;

/* Hover transform */
transform: translateY(-5px);

/* Modal animation */
@keyframes modalFade {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

## Usage Notes

1. **Color Theme**: Use the forest green (`#28a745`) as the primary action color and warm beige (`#FAF7F2`) for backgrounds.

2. **Typography**: Stick to Montserrat for headings and Poppins for body text.

3. **Spacing**: Use multiples of 0.5rem for consistent spacing (0.5rem, 1rem, 1.5rem, 2rem, etc.).

4. **Shadows**: Use consistent shadow values for depth:
   - Light: `0 2px 4px rgba(0, 0, 0, 0.1)`
   - Medium: `0 4px 6px rgba(0, 0, 0, 0.1)`
   - Heavy: `0 8px 16px rgba(0, 0, 0, 0.15)`

5. **Border Radius**: Use consistent border-radius values:
   - Small: `5px`
   - Medium: `10px`
   - Large: `16px`