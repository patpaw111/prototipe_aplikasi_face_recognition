import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import LoginPage from './pages/LoginPage.jsx';
import ErrorPage from './pages/ErrorPage.jsx';
import Kasir from './pages/Kasir.jsx';

const router = createBrowserRouter([
  {
    path: "/",
    element: <div>Hello, World!</div>,
    errorElement: <ErrorPage />,
  },
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/kasir",
    element: <Kasir />,
  },
]);

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
);
