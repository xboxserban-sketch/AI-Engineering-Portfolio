export function StatusBar({ status }: { status: string }) {
  return (
    <div className="bg-gray-800 p-4 rounded-lg mt-6 flex justify-between items-center border border-gray-700">
      <span className="text-gray-400">Swarm Status:</span>
      <span className={`font-bold uppercase ${status === 'completed' ? 'text-green-400' : 'text-yellow-400'}`}>{status}</span>
    </div>
  );
}
