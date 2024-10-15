'use client'
import { useState } from 'react';
import SearchBar from '../components/SearchBar';
import FileUpload from '../components/FileUpload';
import axios from 'axios';
import { motion } from 'framer-motion';
import Layout from '@/components/Layout';
interface SearchResult {
  type: string;
  content: string;
  similarity: number;
}

export default function Home() {
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (query: string) => {
    setIsLoading(true);
    try {
      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/search`, { text: query });
      setSearchResults(response.data.results);
    } catch (error) {
      console.error('Error searching:', error);
    }
    setIsLoading(false);
  };

  const handleFileUpload = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/documents`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert('File uploaded successfully!');
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file');
    }
  };

  return (
<Layout>
    <SearchBar onSearch={handleSearch} />
      <FileUpload onFileUpload={handleFileUpload} />
      {isLoading ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-8 text-center"
        >
          Loading...
        </motion.div>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-8"
        >
          {searchResults.map((result, index) => (
            <motion.div
              key={index}
              initial={{ y: 50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white shadow overflow-hidden sm:rounded-lg mb-4"
            >
              <div className="px-4 py-5 sm:px-6">
                <h3 className="text-lg leading-6 font-medium text-gray-900">
                  {result.type}
                </h3>
                <p className="mt-1 max-w-2xl text-sm text-gray-500">
                  Similarity: {result.similarity.toFixed(2)}
                </p>
              </div>
              <div className="border-t border-gray-200">
                <dl>
                  <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt className="text-sm font-medium text-gray-500">Content</dt>
                    <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                      {result.content}
                    </dd>
                  </div>
                </dl>
              </div>
            </motion.div>
          ))}
        </motion.div>
      )}
</Layout>
  );
}