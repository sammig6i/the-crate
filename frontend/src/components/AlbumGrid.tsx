import { SimpleGrid, Box, Image, Text, VStack, Badge } from '@chakra-ui/react'
import { useQuery } from '@tanstack/react-query'
import { Link as RouterLink } from 'react-router-dom'
import { fetchAlbums } from '../api/albums'

const AlbumGrid = () => {
  const { data: albums, isLoading, error } = useQuery({
    queryKey: ['albums'],
    queryFn: fetchAlbums,
  })

  if (isLoading) {
    return <Text>Loading albums...</Text>
  }

  if (error) {
    return <Text color="red.500">Error loading albums</Text>
  }

  return (
    <SimpleGrid columns={{ base: 2, md: 3, lg: 4 }} spacing={6}>
      {albums?.map((album) => (
        <Box
          key={album.id}
          as={RouterLink}
          to={`/albums/${album.id}`}
          borderRadius="lg"
          overflow="hidden"
          transition="transform 0.2s"
          _hover={{ transform: 'scale(1.02)' }}
          bg="white"
          shadow="md"
        >
          <Image
            src={album.coverUrl || 'https://via.placeholder.com/300'} // Replace with actual album cover
            alt={album.title}
            width="100%"
            height="300px"
            objectFit="cover"
          />
          <VStack p={4} align="start" spacing={1}>
            <Text fontWeight="bold" fontSize="lg" noOfLines={1}>
              {album.title}
            </Text>
            <Text color="gray.600" fontSize="md" noOfLines={1}>
              {album.artist}
            </Text>
            <Badge colorScheme={getStatusColor(album.status)}>{album.status}</Badge>
          </VStack>
        </Box>
      ))}
    </SimpleGrid>
  )
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'approved':
      return 'green'
    case 'pending':
      return 'yellow'
    case 'rejected':
      return 'red'
    default:
      return 'gray'
  }
}

export default AlbumGrid 