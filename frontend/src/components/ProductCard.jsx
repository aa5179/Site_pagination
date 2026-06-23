export default function ProductCard({ product }) {
  return (
    <div className="bg-white rounded-2xl shadow-md border border-gray-200 p-5 hover:shadow-lg transition">
      <h2 className="text-xl font-bold text-gray-900 mb-2">{product.name}</h2>

      <div className="text-sm text-blue-600 font-medium mb-2">
        {product.category}
      </div>

      <div className="text-2xl font-bold text-gray-800 mb-3">
        ₹{product.price}
      </div>

      <div className="text-xs text-gray-500">
        Updated: {new Date(product.updated_at).toLocaleString()}
      </div>
    </div>
  );
}
