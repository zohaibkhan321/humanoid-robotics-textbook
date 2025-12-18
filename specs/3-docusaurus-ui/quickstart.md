# Quickstart: Docusaurus UI Improvements

## Prerequisites
- Node.js (v16 or higher)
- npm or yarn package manager
- Git for version control

## Setup Development Environment

1. **Install dependencies**:
   ```bash
   cd website
   npm install
   ```

2. **Start development server**:
   ```bash
   npm start
   ```
   This will start the development server at http://localhost:3000

## Implementation Steps

### 1. Remove Blog Plugin
- Edit `website/docusaurus.config.js`
- Find the `presets` section under `'classic'`
- Remove or comment out the `blog: { ... }` configuration
- Remove blog-related items from navbar and footer

### 2. Update Home Page Button
- Edit `website/src/pages/index.js`
- Modify the Link component in the HomepageHeader function
- Change the `to` prop to point to relevant documentation (e.g., `/docs/intro`)

### 3. Add Social Links to Footer
- Edit `website/docusaurus.config.js`
- In the `footer.links` array, add a new section for social links
- Include GitHub and LinkedIn links with proper URLs

### 4. Configure GitHub Pages Deployment
- Edit `website/docusaurus.config.js`
- Update `url` to your GitHub Pages URL
- Update `baseUrl` if needed (usually `/` for project pages)
- Set `organizationName` to your GitHub username
- Set `projectName` to your repository name

## Testing Changes

1. **Local Testing**:
   ```bash
   npm start
   ```
   Verify all changes appear correctly in the browser

2. **Build Testing**:
   ```bash
   npm run build
   ```
   Ensure the site builds without errors

3. **Preview Build**:
   ```bash
   npm run serve
   ```
   Preview the production build locally

## Deployment

1. **Build the site**:
   ```bash
   npm run build
   ```

2. **Deploy to GitHub Pages**:
   ```bash
   npm run deploy
   ```

This will deploy the site to your configured GitHub Pages URL.