const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
export async function getProducts(cursor = null, category = null) {
  let url = `${API_URL}/products?limit=20`;

  if (cursor) {
    url += `&cursor=${encodeURIComponent(cursor)}`;
  }

  if (category) {
    url += `&category=${encodeURIComponent(category)}`;
  }

  const response = await fetch(url);
  return response.json();
}
