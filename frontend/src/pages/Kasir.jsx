import React, { useState, useRef } from "react";
import Webcam from "react-webcam";

const App = () => {
  const [menuList] = useState(["Ayam geprek", "mie goreng geprek", "es teh", "es jeruk"]); // Menu tersedia
  const [selectedMenu, setSelectedMenu] = useState([]); // Menu yang dipilih
  const webcamRef = useRef(null);

  // Tambahkan item ke daftar menu yang dipilih
  const addToOrder = (item) => {
    setSelectedMenu((prev) => [...prev, item]);
  };

  // Hapus item dari daftar menu yang dipilih
  const removeFromOrder = (index) => {
    const newSelectedMenu = [...selectedMenu];
    newSelectedMenu.splice(index, 1);
    setSelectedMenu(newSelectedMenu);
  };

  // Fungsi untuk mengambil foto dari kamera
  const capturePhoto = () => {
    if (webcamRef.current) {
      return webcamRef.current.getScreenshot();
    }
    return null;
  };

  // Fungsi untuk memproses order
  const handleOrder = async () => {
    const photos = [];
    for (let i = 0; i < 20; i++) {
      const photo = capturePhoto();
      if (photo) photos.push(photo);
    }

    if (photos.length < 20) {
      alert("Failed to capture 20 photos. Please try again.");
      return;
    }

    const payload = {
      menu: selectedMenu,
      photos,
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/order", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      // Tampilkan modal hasil
      alert(
        `Order Successful!\nMenu: ${data.menu.join(", ")}\nExpression: ${data.expression}`
      );

      // Reset daftar pesanan
      setSelectedMenu([]);
    } catch (error) {
      alert("Order failed! Please try again.");
      console.error(error);
    }
  };

  // Fungsi untuk membatalkan semua pesanan
  const cancelOrder = () => {
    setSelectedMenu([]);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
      <h1 className="text-2xl font-bold mb-4">Prototype sistem pendeteksi kepuasan pelanggan</h1>

      <div className="grid grid-cols-3 gap-4 w-full max-w-6xl">
        {/* Kamera */}
        <div className="bg-white p-4 rounded shadow flex flex-col items-center">
          <h2 className="text-xl font-semibold mb-2">Camera</h2>
          <Webcam
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            className="w-full h-64 rounded"
          />
        </div>

        {/* Menu Tersedia */}
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold mb-2">Menu</h2>
          <ul>
            {menuList.map((item, index) => (
              <li
                key={index}
                className="py-2 px-4 border-b flex justify-between items-center"
              >
                {item}
                <button
                  onClick={() => addToOrder(item)}
                  className="bg-green-500 text-white px-3 py-1 rounded"
                >
                  Add
                </button>
              </li>
            ))}
          </ul>
        </div>

        {/* Daftar Pesanan */}
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold mb-2">Selected Menu</h2>
          <ul>
            {selectedMenu.map((item, index) => (
              <li
                key={index}
                className="py-2 px-4 border-b flex justify-between items-center"
              >
                {item}
                <button
                  onClick={() => removeFromOrder(index)}
                  className="bg-red-500 text-white px-3 py-1 rounded"
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
          <div className="mt-4">
            <button
              onClick={handleOrder}
              className="bg-blue-500 text-white px-4 py-2 rounded mr-2"
            >
              Order
            </button>
            <button
              onClick={cancelOrder}
              className="bg-gray-500 text-white px-4 py-2 rounded"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
