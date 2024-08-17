import Image from "next/image";
import Link from "next/link";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  return (
    <main>
      <h1 className="text-5xl font-bold">Hello World</h1>
      <Link href="/stock_display" passHref>
        <button style={{ padding: '10px 20px', fontSize: '16px', cursor: 'pointer' }}>
          Go to Stock Display
        </button>
      </Link>
    </main>
  );
}
