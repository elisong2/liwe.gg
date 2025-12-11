// "use client";

// import { useState } from "react";

// type PaginationProps<T> = {
//   data: T[];
//   pageSize?: number;
//   render: (item: T, index: number) => React.ReactNode;
// };

// export function Pagination<T>({
//   data,
//   pageSize = 10,
//   render,
// }: PaginationProps<T>) {
//   const [page, setPage] = useState(1);

//   const totalPages = Math.ceil(data.length / pageSize);
//   const start = (page - 1) * pageSize;
//   const currentPageData = data.slice(start, start + pageSize);

//   return (
//     <div>
//       <div className="space-y-2">
//         {currentPageData.map((item, i) => render(item, start + i))}
//       </div>

//       <div className="flex justify-center gap-2 mt-4">
//         <button
//           disabled={page === 1}
//           onClick={() => setPage((p) => p - 1)}
//           className="px-3 py-1 rounded bg-gray-200 disabled:opacity-50"
//         >
//           Prev
//         </button>
//         <span className="px-3 py-1">
//           Page {page} / {totalPages}
//         </span>
//         <button
//           disabled={page === totalPages}
//           onClick={() => setPage((p) => p + 1)}
//           className="px-3 py-1 rounded bg-gray-200 disabled:opacity-50"
//         >
//           Next
//         </button>
//       </div>
//     </div>
//   );
// }
