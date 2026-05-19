export default function LoadingSpinner({ message = 'Loading...' }: { message?: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 gap-4">
      <div className="relative w-12 h-12">
        <div className="absolute inset-0 rounded-full border-2 border-[rgba(124,58,237,0.2)]" />
        <div className="absolute inset-0 rounded-full border-2 border-transparent border-t-[#7c3aed] animate-spin"
          style={{ boxShadow: '0 0 12px rgba(124,58,237,0.4)' }}
        />
      </div>
      <p className="text-[#a89fc4] text-sm font-light tracking-wide">{message}</p>
    </div>
  )
}
