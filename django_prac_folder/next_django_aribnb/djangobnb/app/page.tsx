import Image from "next/image";

export default function Home() {
  return (
    <main className="">
      DjangoBnb Set

      {/* In tailwind.css it is convention to set bg-<somecolor> or text-<somecolor>.
        Since inside of 'tailwind.config.ts' i have changed 'colors' dictionary to my
        custom class name with custom color, i can use 'aribnb'.
      */}
      <h2 className="bg-aribnb">DjangoAribnb</h2>

    </main>
  );
}
