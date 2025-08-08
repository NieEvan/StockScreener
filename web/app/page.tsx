import { Link } from "@heroui/link";
import { Button } from "@heroui/button";
import { title, subtitle } from "@/components/primitives";

export default function Home() {
  return (
    <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
      <div className="inline-block max-w-lg text-center justify-center">
        <h1 className={title()}>Real-time&nbsp;</h1>
        <h1 className={title({ color: "violet" })}>Stock Screener&nbsp;</h1>
        <h1 className={title()}>
          Platform
        </h1>
        <h2 className={subtitle({ class: "mt-4" })}>
          Monitor stocks and receive real-time alerts on price movements, breakouts, and market shifts.
        </h2>
      </div>

      <div className="flex gap-3">
        <Button
          as={Link}
          color="primary"
          href="/dashboard"
          variant="solid"
        >
          Go to Dashboard
        </Button>
        <Button
          as={Link}
          color="default"
          href="/docs"
          variant="bordered"
        >
          Documentation
        </Button>
      </div>

      <div className="mt-8">
        <div className="flex flex-col gap-8 items-center justify-center">
          <div className="max-w-3xl p-6 bg-default-50 border border-default-200 rounded-lg">
            <h3 className="text-lg font-semibold mb-2">Features</h3>
            <ul className="list-disc list-inside space-y-2">
              <li>Real-time stock alerts via WebSocket</li>
              <li>Interactive candlestick charts powered by TradingView's Lightweight Charts</li>
              <li>Multiple timeframe support (1M, 5M, 1H, 4H)</li>
              <li>Customizable alerts based on technical indicators</li>
              <li>Support for various markets and symbols</li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
