"use client";
import React, { useState } from 'react';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import { toast } from '../../components/ui/toast';

const Upload_Content: React.FC = () => {
  const [description, setDescription] = useState('');
  const [isSubmitEnabled, setIsSubmitEnabled] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const baseURL = "https://62dc-202-134-191-26.ngrok-free.app/api/postcontext/krish"; // Update with your actual API URL

  const sendToApi = async (context: string) => {
    try {
      const apiEndpoint = process.env.NEXT_PUBLIC_API_ENDPOINT || baseURL;
      console.log("API Endpoint:", apiEndpoint);
      
      const response = await axios.post(apiEndpoint, { context }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      return response.data;
    } catch (error) {
      console.error('Error in sendToApi:', error.response ? error.response.data : error.message);
      throw new Error('Failed to send data to API');
    }
  };
  
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!isSubmitEnabled || isLoading) return;

    setIsLoading(true);
    try {
      console.log('Sending to API...');
      await sendToApi(description);
      console.log('API submission successful');

      toast({
        title: "Success",
        description: "Your content has been uploaded successfully.",
        duration: 3000,
      });

      router.push("/");
    } catch (error) {
      console.error('Error in form submission:', error);
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to upload content",
        variant: "destructive",
        duration: 5000,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleDescriptionChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    setDescription(value);
    setIsSubmitEnabled(!!value.trim());
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-2xl mx-auto p-6 space-y-6">
      <div className="space-y-4">
        <div className="space-y-2">
          <label
            htmlFor="description"
            className="block text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Description
          </label>
          <Textarea
            id="description"
            placeholder="Enter your text here..."
            value={description}
            onChange={handleDescriptionChange}
            className="min-h-[200px] w-full"
            disabled={isLoading}
          />
        </div>
        
        <Button
          type="submit"
          className="w-full bg-blue-600 hover:bg-blue-700 transition-colors"
          disabled={!isSubmitEnabled || isLoading}
        >
          {isLoading ? (
            <span className="flex items-center space-x-2">
              <span className="animate-spin">⌛</span>
              <span>Uploading...</span>
            </span>
          ) : (
            'Submit'
          )}
        </Button>
      </div>
    </form>
  );
};

export default Upload_Content;
