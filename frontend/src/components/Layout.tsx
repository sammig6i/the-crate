import { Box, Container, Flex, Link as ChakraLink, Heading } from '@chakra-ui/react'
import { Link as RouterLink } from 'react-router-dom'

interface LayoutProps {
  children: React.ReactNode
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <Box minH="100vh">
      <Box bg="gray.800" color="white" py={4}>
        <Container maxW="container.xl">
          <Flex justify="space-between" align="center">
            <ChakraLink as={RouterLink} to="/" _hover={{ textDecoration: 'none' }}>
              <Heading size="lg">The Crate</Heading>
            </ChakraLink>
            <Flex gap={4}>
              <ChakraLink as={RouterLink} to="/" _hover={{ color: 'gray.300' }}>
                Albums
              </ChakraLink>
              <ChakraLink as={RouterLink} to="/admin" _hover={{ color: 'gray.300' }}>
                Admin
              </ChakraLink>
            </Flex>
          </Flex>
        </Container>
      </Box>
      <Container maxW="container.xl" py={8}>
        {children}
      </Container>
    </Box>
  )
}

export default Layout 