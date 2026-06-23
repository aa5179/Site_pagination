import { useEffect, useState } from "react";
import { getProducts } from "./api";
import ProductCard from "./components/ProductCard";

export default function App() {
  const [products, setProducts] = useState([]);
  const [cursor, setCursor] = useState(null);
  const [snapshotTime, setSnapshotTime] = useState(null);
  const [category, setCategory] = useState("");

  async function loadProducts(reset = false) {
    const data = await getProducts(reset ? null : cursor, category || null);

    if (reset) {
      setProducts(data.products);
    } else {
      setProducts((prev) => [...prev, ...data.products]);
    }

    setCursor(data.next_cursor);
    setSnapshotTime(data.snapshot_time);
  }

  useEffect(() => {
    loadProducts(true);
  }, []);

  async function applyFilter() {
    setCursor(null);
    await loadProducts(true);
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto px-6 py-10">
        {/* Header */}

        <h1 className="text-5xl font-bold text-center text-black mb-2">
          Product Browser
        </h1>

        <p className="text-center text-gray-600 mb-8">
          Browse 200,000+ products using Cursor + Snapshot Pagination
        </p>

        {/* Snapshot Badge */}

        {snapshotTime && (
          <div className="flex justify-center mb-6">
            <div className="px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
              Snapshot: {new Date(snapshotTime).toLocaleString()}
            </div>
          </div>
        )}

        {/* Filters */}

        <div className="flex justify-center gap-3 mb-6">
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="border rounded-lg px-4 py-2 bg-white"
          >
            <option value="">All Categories</option>

            <option value="Electronics">Electronics</option>

            <option value="Clothing">Clothing</option>

            <option value="Sports">Sports</option>

            <option value="Comics">Comics</option>

            <option value="Marvel Figurines">Marvel Figurines</option>

            <option value="Home & Kitchen">Home & Kitchen</option>
          </select>

          <button
            onClick={applyFilter}
            className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg"
          >
            Apply Filter
          </button>
        </div>

        {/* Stats */}

        <div className="text-center text-gray-600 mb-8">
          Products Loaded: <span className="font-bold">{products.length}</span>
        </div>

        {/* Product Grid */}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>

        {/* Load More */}

        {cursor && (
          <div className="flex justify-center mt-10">
            <button
              onClick={() => loadProducts(false)}
              className="bg-black text-white px-6 py-3 rounded-xl hover:bg-gray-800"
            >
              Load More Products
            </button>
          </div>
        )}

        {/* Footer */}

        <div className="text-center text-gray-500 text-sm mt-12">
          200,000 Products • Cursor Pagination • Snapshot Pagination
        </div>
      </div>
    </div>
  );
}
